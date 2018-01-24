# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy import Request
from scrapy.exceptions import IgnoreRequest


class GGDownloaderMiddleware(object):
    def process_response(self, request, response, spider):
        if response.css('head').re('<script[^<>]*>\s*setTimeout[^<>]+location[.]replace[^<>]+</script>'):
            return request.replace(dont_filter=True)
        else:
            if spider.routines:
                spider.routines.pop(0)
            if response.status in [404, 403]:
                if spider.requests:
                    r = spider.requests.pop(0)
                    spider.routines.append(r)
                    return r
                else:
                    n = spider.request_next()
                    if n is not None:
                        return n
                    else:
                        raise IgnoreRequest()
            return response


class GGSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            if isinstance(i, Request):
                spider.requests.append(i)
            else:
                yield i
        if not spider.routines:
            if spider.requests:
                request = spider.requests.pop(0)
                spider.routines.append(request)
                yield request

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            spider.requests.append(r)
        if not spider.routines:
            if spider.requests:
                r = spider.requests.pop(0)
                spider.routines.append(r)
                yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
