from scrapy import Request
from scrapy import FormRequest
from scrapy.spiders import CrawlSpider

from ggmssql.pool import Pool
import config


# 公共Spider基类
class GGSpider(CrawlSpider):
    channel = None
    groupname = None

    handle_httpstatus_list = [404]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        # 'REDIRECT_ENABLED': True,
        # 'ITEM_PIPELINES': {'GGScrapy.pipelines.GGPipeline': 300}
    }

    def __init__(self, *args, **kwargs):
        super(GGSpider, self).__init__(*args, **kwargs)

    @staticmethod
    def parse_cookies(cookies):
        if cookies is not None:
            ret = {}
            cks = cookies.split(';')
            for ck in cks:
                ck = ck.split('=', 1)
                key = ck[0].strip()
                value = ck[1].strip()
                ret[key] = value
            cookies = ret
        return cookies


# 新闻资讯Spider基类
class GGNewsSpider(GGSpider):
    channel = '-'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
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

    def request_next(self, cps, rcs, nps):
        while len(cps) >= 1:
            cp = cps.pop(0)
            ext = cp['ext'] if 'ext' in cp else {}

            pg = cp['pg'] if 'pg' in cp else None
            url = cp['url'] if 'url' in cp else None
            url = url(pg) if callable(url) else url

            cookies = cp['cookies'] if 'cookies' in cp else None
            cookies = self.parse_cookies(cookies)

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               cookies=cookies,
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_link)

        while len(rcs) >= 1:
            rc = rcs.pop(0)
            ext = rc['ext'] if 'ext' in rc else {}

            pg = rc['pg'] if 'pg' in rc else None
            url = rc['url'] if 'url' in rc else None
            url = url(pg) if callable(url) else url

            cookies = rc['cookies'] if 'cookies' in rc else None
            cookies = self.parse_cookies(cookies)

            count = rc['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, dont_filter=True,
                               headers={'Referer': rc['ref']},
                               cookies=cookies,
                               meta={'ch': rc['ch'], 'pg': pg, 'url': rc['url'],
                                     'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_item)

        cps = nps
        nps = []
        while len(cps) >= 1:
            cp = cps.pop(0)
            ext = cp['ext'] if 'ext' in cp else {}

            pg = cp['pg'] if 'pg' in cp else None
            url = cp['url'] if 'url' in cp else None
            url = url(pg) if callable(url) else url

            cookies = cp['cookies'] if 'cookies' in cp else None
            cookies = self.parse_cookies(cookies)

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               cookies=cookies,
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_link)

    def parse_link(self, response):
        pass

    def parse_item(self, response):
        pass


# 基金净值Spider基类
class GGFundNavSpider(GGSpider):
    channel = '基金净值'
    groupname = 'scrapy'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGFundNavPipeline': 300}
    }

    dbPool = Pool(config.fund_nav['db']['host'],
                  config.fund_nav['db']['port'],
                  config.fund_nav['db']['user'],
                  config.fund_nav['db']['pswd'],
                  config.fund_nav['db']['name'],
                  timeout=config.fund_nav['db']['timeout'])

    def __init__(self, *args, **kwargs):
        super(GGFundNavSpider, self).__init__(*args, **kwargs)

    def request_next(self, fps, ips):
        while len(ips) >= 1:
            ip = ips.pop(0)
            ext = ip['ext'] if 'ext' in ip else {}

            headers = ip['headers'] if 'headers' in ip else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = ip['ref']

            cookies = ip['cookies'] if 'cookies' in ip else None
            cookies = self.parse_cookies(cookies)

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
                                   headers=headers, cookies=cookies,
                                   meta={'pg': pg, 'url': ip['url'], 'form': form,
                                         'fps': fps, 'ips': ips, 'ext': ext},
                                   callback=self.parse_item)
            else:
                return Request(url, dont_filter=True,
                               headers=headers, cookies=cookies,
                               meta={'pg': pg, 'url': ip['url'], 'form': None,
                                     'fps': fps, 'ips': ips, 'ext': ext},
                               callback=self.parse_item)

        while len(fps) >= 1:
            fp = fps.pop(0)
            ext = fp['ext'] if 'ext' in fp else {}

            headers = fp['headers'] if 'headers' in fp else {}
            headers = headers if isinstance(headers, dict) else {}
            headers['Referer'] = fp['ref']

            cookies = fp['cookies'] if 'cookies' in fp else None
            cookies = self.parse_cookies(cookies)

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
                                   headers=headers, cookies=cookies,
                                   meta={'pg': pg, 'url': fp['url'], 'form': form,
                                         'fps': fps, 'ips': ips, 'ext': ext},
                                   callback=self.parse_fund)
            else:
                return Request(url, priority=1,
                               headers=headers, cookies=cookies,
                               meta={'pg': pg, 'url': fp['url'], 'form': None,
                                     'fps': fps, 'ips': ips, 'ext': ext},
                               callback=self.parse_fund)

    def parse_fund(self, response):
        pass

    def parse_item(self, response):
        pass
