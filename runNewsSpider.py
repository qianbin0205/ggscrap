from scrapy import cmdline


# cmdline.execute(['scrapy', 'crawl', 'News_ZzwCs', '-a', 'limit=50', '-a', 'jobId=0L'])
# cmdline.execute(['scrapy', 'crawl', 'News_Cnstock', '-a', 'limit=50', '-a', 'jobId=0L'])
# cmdline.execute(['scrapy', 'crawl', 'News_Ccstock', '-a', 'limit=50', '-a', 'jobId=0L'])
cmdline.execute(['scrapy', 'crawl', 'News_Stcn', '-a', 'limit=50', '-a', 'jobId=0L'])