from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'Interaction_SseInfo', '-a', 'jobId=0L'])

# cmdline.execute(['scrapy', 'crawl', 'News_Hexun', '-a', 'limit=50', '-a', 'jobId=0L'])
