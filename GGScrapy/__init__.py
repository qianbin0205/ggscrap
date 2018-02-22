import uuid
from io import StringIO
from scrapy import Request
from scrapy import FormRequest
from scrapy.spiders import CrawlSpider


class MultiPartFormRequest(Request):
    def __init__(self, *args, **kwargs):
        formdata = kwargs.pop('formdata', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(MultiPartFormRequest, self).__init__(*args, **kwargs)

        if formdata:
            boundary = '----WebKitFormBoundary' + uuid.uuid1().hex[0:16]
            self.headers.setdefault('Content-Type', 'multipart/form-data; boundary=' + boundary)

            buffer = StringIO()
            for k, v in formdata.items():
                buffer.write('--{0}\r\n'.format(boundary))
                buffer.write('Content-Disposition: form-data; name="{0}"\r\n'.format(k))
                buffer.write('\r\n')
                buffer.write('{0}\r\n'.format(v))
            buffer.write('--{0}--\r\n'.format(boundary))
            self._set_body(buffer.getvalue())


# 公共Spider基类
class GGSpider(CrawlSpider):
    sitename = None
    channel = None
    groupname = 'GGScrapy'

    handle_httpstatus_list = [404]
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'ITEM_PIPELINES': {'GGScrapy.pipelines.GGPipeline': 300},
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

            mform = pi['mform'] if 'mform' in pi else None
            if mform is not None:
                formdata = {}
                for (k, v) in mform.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return MultiPartFormRequest(url=req_url, headers=headers, dont_filter=True, callback=pf,
                                            formdata=formdata,
                                            meta={'pi': pi,
                                                  'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                                  'headers': headers, 'mform': mform})

            form = pi['form'] if 'form' in pi else None
            if form is not None:
                formdata = {}
                for (k, v) in form.items():
                    v = v(pg) if callable(v) else v
                    formdata[k] = v
                return FormRequest(url=req_url, headers=headers, dont_filter=True, callback=pf,
                                   formdata=formdata,
                                   meta={'pi': pi,
                                         'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                         'headers': headers, 'form': form})

            body = pi['body'] if 'body' in pi else None
            body = body(pg) if callable(body) else body
            method = 'POST' if body else 'GET'
            return Request(req_url, method=method, headers=headers, dont_filter=True, callback=pf,
                           body=body,
                           meta={'pi': pi,
                                 'ext': ext, 'pg': pg, 'url': url, 'ref': ref,
                                 'headers': headers, 'body': body})

    def parse_list(self, response):
        pass

    def parse_item(self, response):
        pass
