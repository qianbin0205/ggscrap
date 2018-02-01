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
    lps = []  # list pages
    ips = []  # item pages

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

    def request_next(self):
        ps = self.ips or self.lps  # pages
        pf = self.parse_item if self.ips else self.parse_list  # parse function
        if ps:
            pi = ps.pop(0)  # page info

            ext = pi['ext'] if 'ext' in pi else {}
            pg = pi['pg'] if 'pg' in pi else None

            url = pi['url'] if 'url' in pi else None
            req_url = url(pg) if callable(url) else url

            ref = pi['ref'] if 'ref' in pi else None
            req_ref = ref(pg) if callable(ref) else ref

            headers = pi['headers'] if 'headers' in pi else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = req_ref

            form = pi['form'] if 'form' in pi else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=req_url, headers=headers, formdata=formdata, dont_filter=True, callback=pf,
                                   meta={'pi': pi,
                                         'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                         'headers': headers, 'form': form})
            else:
                body = pi['body'] if 'body' in pi else None
                body = body(pg) if callable(body) else body
                method = 'POST' if body else 'GET'
                return Request(req_url, method=method, headers=headers, body=body, dont_filter=True, callback=pf,
                               meta={'pi': pi,
                                     'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                     'headers': headers, 'body': body})

    def parse_list(self, response):
        pass

    def parse_item(self, response):
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

    def __init__(self, limit=None, *args, **kwargs):
        super(GGNewsSpider, self).__init__(*args, **kwargs)
        try:
            limit = int(limit)
        except:
            self.__limit = None
        else:
            if limit > 0:
                self.__limit = limit
            else:
                if limit < 0:
                    self.__limit = -limit
                else:
                    self.__limit = None

    @property
    def limit(self):
        return self.__limit

    def request_next(self):
        ps = self.ips or self.lps  # pages
        if ps:
            pi = ps[0]
            ch = pi['ch'] if 'ch' in pi else {}
            count = ch['count'] if 'count' in ch else 0
            count = count if isinstance(count, int) else 0
            if self.limit and count >= self.limit:
                ps.pop(0)
            return super(GGNewsSpider, self).request_next()


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

    fps = []  # fund (list) pages
    ips = []  # item (list) pages

    def __init__(self, *args, **kwargs):
        super(GGFundNavSpider, self).__init__(*args, **kwargs)

    def request_next(self, *args):
        self.fps = args[0] if args[0:] else self.fps
        self.ips = args[1] if args[1:] else self.ips

        ps = self.ips or self.fps  # pages
        pf = self.parse_item if self.ips else self.parse_fund  # parse function
        if ps:
            pi = ps.pop(0)  # page info

            ext = pi['ext'] if 'ext' in pi else {}
            pg = pi['pg'] if 'pg' in pi else None

            url = pi['url'] if 'url' in pi else None
            req_url = url(pg) if callable(url) else url

            ref = pi['ref'] if 'ref' in pi else None
            req_ref = ref(pg) if callable(ref) else ref

            headers = pi['headers'] if 'headers' in pi else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = req_ref

            form = pi['form'] if 'form' in pi else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=req_url, headers=headers, formdata=formdata, dont_filter=True, callback=pf,
                                   meta={'pi': pi,
                                         'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                         'headers': headers, 'form': form,
                                         'fps': self.fps, 'ips': self.ips})
            else:
                body = pi['body'] if 'body' in pi else None
                body = body(pg) if callable(body) else body
                method = 'POST' if body else 'GET'
                return Request(req_url, method=method, headers=headers, body=body, dont_filter=True, callback=pf,
                               meta={'pi': pi,
                                     'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                     'headers': headers, 'body': body,
                                     'fps': self.fps, 'ips': self.ips})

    def parse_fund(self, response):
        pass

    def parse_item(self, response):
        pass


# 基金公告Spider基类
class GGFundNoticeSpider(GGSpider):
    channel = '公告'

    custom_settings = {
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGFundNoticePipeline': 300}
    }

    dbPool = Pool(config.fund_notice['db']['host'],
                  config.fund_notice['db']['port'],
                  config.fund_notice['db']['user'],
                  config.fund_notice['db']['pswd'],
                  config.fund_notice['db']['name'],
                  timeout=config.fund_notice['db']['timeout'])

    def __init__(self, *args, **kwargs):
        super(GGFundNoticeSpider, self).__init__(*args, **kwargs)


# 投资者关系互动平台Spider基类
class GGInteractionSpider(GGSpider):
    custom_settings = {
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGInteractionPipeline': 300}
    }

    dbPool = Pool(config.interaction['db']['host'],
                  config.interaction['db']['port'],
                  config.interaction['db']['user'],
                  config.interaction['db']['pswd'],
                  config.interaction['db']['name'],
                  timeout=config.interaction['db']['timeout'])

    def __init__(self, *args, **kwargs):
        super(GGInteractionSpider, self).__init__(*args, **kwargs)
