from scrapy import cmdline

# cmdline.execute(['scrapy', 'crawl', 'FundNav_ChuangYingtz', '-a', 'jobId=0L'])

cmdline.execute(['scrapy', 'crawl', 'News_Cnfol', '-a', 'limit=50', '-a', 'jobId=0L'])