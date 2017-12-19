from scrapy import cmdline


# cmdline.execute(['scrapy', 'crawl', 'ZzwCsNews', '-a', 'limit=50', '-a', 'jobId=0L'])

cmdline.execute(['scrapy', 'crawl', 'GZDaShuFundNav', '-a', 'jobId=0L'])
