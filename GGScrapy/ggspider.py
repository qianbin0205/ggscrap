from scrapy import Request
from scrapy import FormRequest
from scrapy.spiders import CrawlSpider

from ggmssql.pool import Pool
import config


# 公共Spider基类
class GGSpider(CrawlSpider):
    sitename = None
    channel = None
    groupname = 'GGScrapy'

    handle_httpstatus_list = [404]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'SPIDER_MIDDLEWARES': {'GGScrapy.middlewares.GGSpiderMiddleware': 543},
        'DOWNLOADER_MIDDLEWARES': {'GGScrapy.middlewares.GGDownloaderMiddleware': 543},
    }

    allowed_domains = []
    routines = []
    requests = []
    cookies = None
    proxy = None  # http://YOUR_PROXY_IP:PORT
    proxy_auth = None  # USERNAME:PASSWORD
    start_urls = []

    @staticmethod
    def parse_cookies(cookies):
        if isinstance(cookies, str):
            dct = {}
            cks = cookies.split(';')
            for ck in cks:
                ck = ck.split('=', 1)
                key = ck[0].strip()
                value = ck[1].strip()
                dct[key] = value
            cookies = dct
        if isinstance(cookies, dict):
            lst = []
            for k, v in cookies.items():
                lst.append({
                    'name': k,
                    'value': v,
                    'path': '/'
                })
            cookies = lst
        if isinstance(cookies, list):
            for item in cookies:
                item['path'] = '/'
        else:
            cookies = {}
        return cookies

    @classmethod
    def update_settings(cls, settings):
        mro = cls.mro()
        i = mro.index(GGSpider)
        rro = mro[i::-1]
        for c in rro:
            settings.setdict(c.custom_settings or {}, priority='spider')

    def __init__(self, *args, **kwargs):
        super(GGSpider, self).__init__(*args, **kwargs)
        self.cookies = self.parse_cookies(self.cookies)

    def start_requests(self):
        yield self.request_next()

    def request_next(self, *args):
        pass


# 新闻资讯Spider基类
class GGNewsSpider(GGSpider):
    custom_settings = {
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGNewsPipeline': 300}
    }

    dbPool = Pool(config.news['db']['host'],
                  config.news['db']['port'],
                  config.news['db']['user'],
                  config.news['db']['pswd'],
                  config.news['db']['name'],
                  timeout=config.news['db']['timeout'])

    cps = []
    rcs = []
    nps = []

    def __init__(self, limit=None, *args, **kwargs):
        super(GGNewsSpider, self).__init__(*args, **kwargs)
        try:
            limit = int(limit)
        except:
            self.__update = True
            self.__limit = None
        else:
            if limit > 0:
                self.__limit = limit
                self.__update = False
            else:
                self.__update = True
                if limit < 0:
                    self.__limit = -limit
                else:
                    self.__limit = None

    @property
    def update(self):
        return self.__update

    @property
    def limit(self):
        return self.__limit

    def request_next(self, *args):
        self.cps = args[0] if args[0:] else self.cps
        self.rcs = args[1] if args[1:] else self.rcs
        self.nps = args[2] if args[2:] else self.nps

        while self.cps:
            cp = self.cps.pop(0)
            ext = cp['ext'] if 'ext' in cp else {}

            pg = cp['pg'] if 'pg' in cp else None
            url = cp['url'] if 'url' in cp else None
            url = url(pg) if callable(url) else url

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': self.cps, 'rcs': self.rcs, 'nps': self.nps, 'ext': ext},
                               callback=self.parse_link)

        while self.rcs:
            rc = self.rcs.pop(0)
            ext = rc['ext'] if 'ext' in rc else {}

            pg = rc['pg'] if 'pg' in rc else None
            url = rc['url'] if 'url' in rc else None
            url = url(pg) if callable(url) else url

            count = rc['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, dont_filter=True,
                               headers={'Referer': rc['ref']},
                               meta={'ch': rc['ch'], 'pg': pg, 'url': rc['url'],
                                     'cps': self.cps, 'rcs': self.rcs, 'nps': self.nps, 'ext': ext},
                               callback=self.parse_item)

        self.cps = self.nps
        self.nps = []
        while self.cps:
            cp = self.cps.pop(0)
            ext = cp['ext'] if 'ext' in cp else {}

            pg = cp['pg'] if 'pg' in cp else None
            url = cp['url'] if 'url' in cp else None
            url = url(pg) if callable(url) else url

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': self.cps, 'rcs': self.rcs, 'nps': self.nps, 'ext': ext},
                               callback=self.parse_link)

    def parse_link(self, response):
        pass

    def parse_item(self, response):
        pass


# 基金净值Spider基类
class GGFundNavSpider(GGSpider):
    custom_settings = {
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGFundNavPipeline': 300}
    }

    dbPool = Pool(config.fund_nav['db']['host'],
                  config.fund_nav['db']['port'],
                  config.fund_nav['db']['user'],
                  config.fund_nav['db']['pswd'],
                  config.fund_nav['db']['name'],
                  timeout=config.fund_nav['db']['timeout'])

    fps = []
    ips = []

    def __init__(self, *args, **kwargs):
        super(GGFundNavSpider, self).__init__(*args, **kwargs)

    def request_next(self, *args):
        self.fps = args[0] if args[0:] else self.fps
        self.ips = args[1] if args[1:] else self.ips

        while self.ips:
            ip = self.ips.pop(0)
            ext = ip['ext'] if 'ext' in ip else {}

            headers = ip['headers'] if 'headers' in ip else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = ip['ref']

            pg = ip['pg'] if 'pg' in ip else None
            url = ip['url'] if 'url' in ip else None
            url = url(pg) if callable(url) else url

            form = ip['form'] if 'form' in ip else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=url, formdata=formdata, dont_filter=True,
                                   headers=headers,
                                   meta={'pg': pg, 'url': ip['url'], 'form': form,
                                         'fps': self.fps, 'ips': self.ips, 'ext': ext},
                                   callback=self.parse_item)
            else:
                return Request(url, dont_filter=True,
                               headers=headers,
                               meta={'pg': pg, 'url': ip['url'], 'form': None,
                                     'fps': self.fps, 'ips': self.ips, 'ext': ext},
                               callback=self.parse_item)

        while self.fps:
            fp = self.fps.pop(0)
            ext = fp['ext'] if 'ext' in fp else {}

            headers = fp['headers'] if 'headers' in fp else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = fp['ref']

            pg = fp['pg'] if 'pg' in fp else None
            url = fp['url'] if 'url' in fp else None
            url = url(pg) if callable(url) else url

            form = fp['form'] if 'form' in fp else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=url, formdata=formdata, priority=1,
                                   headers=headers,
                                   meta={'pg': pg, 'url': fp['url'], 'form': form,
                                         'fps': self.fps, 'ips': self.ips, 'ext': ext},
                                   callback=self.parse_fund)
            else:
                return Request(url, priority=1,
                               headers=headers,
                               meta={'pg': pg, 'url': fp['url'], 'form': None,
                                     'fps': self.fps, 'ips': self.ips, 'ext': ext},
                               callback=self.parse_fund)

    def parse_fund(self, response):
        pass

    def parse_item(self, response):
        pass
