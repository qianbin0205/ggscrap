from scrapy import Request
from scrapy.spiders import CrawlSpider


class GGNewsSpider(CrawlSpider):
    channel = '-'
    groupname = None

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
            url = cp['url']
            url = url(pg) if callable(url) else url

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_list)

        while len(rcs) >= 1:
            rc = rcs.pop(0)
            ext = rc['ext'] if 'ext' in rc else {}

            count = rc['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(rc['url'], dont_filter=True,
                               headers={'Referer': rc['ref']},
                               meta={'ch': rc['ch'], 'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_item)

        cps = nps
        nps = []
        while len(cps) >= 1:
            cp = cps.pop(0)
            ext = cp['ext'] if 'ext' in cp else {}

            pg = cp['pg'] if 'pg' in cp else None
            url = cp['url']
            url = url(pg) if callable(url) else url

            count = cp['ch']['count']
            if self.limit is None or count < self.limit:
                return Request(url, priority=1,
                               headers={'Referer': cp['ref']},
                               meta={'ch': cp['ch'], 'pg': pg, 'url': cp['url'],
                                     'cps': cps, 'rcs': rcs, 'nps': nps, 'ext': ext},
                               callback=self.parse_list)

    def parse_list(self, response):
        pass

    def parse_item(self, response):
        pass
