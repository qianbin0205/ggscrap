from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', '', '-a', 'limit=50', '-a', 'jobId=0L'])
