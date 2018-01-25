from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'FundNav_AshnAsset', '-a', 'jobId=0L'])

# cmdline.execute(['scrapy', 'crawl', 'News_Cnfol', '-a', 'limit=50', '-a', 'jobId=0L'])
