from scrapy import cmdline


cmdline.execute(['scrapy', 'crawl', 'News_ZzwCs', '-a', 'limit=50', '-a', 'jobId=0L'])
