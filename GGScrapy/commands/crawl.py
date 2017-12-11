from scrapy.commands.crawl import Command
from scrapy.exceptions import UsageError
# from scrapy.extensions.closespider import CloseSpider
# from scrapy.exceptions import CloseSpider


class CrawlCommand(Command):
    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        elif len(args) > 1:
            raise UsageError("running 'scrapy crawl' with more than one spider is no longer supported")
        spname = args[0]

        self.crawler_process.crawl(spname, **opts.spargs)

        crawler = list(self.crawler_process.crawlers)[0]
        crawler.stats.set_value('exit_code', 0)

        self.crawler_process.start()

        exitcode = crawler.stats.get_value('exit_code')
        if exitcode != 0:
            if isinstance(exitcode, int):
                self.exitcode = exitcode
            else:
                self.exitcode = 1
