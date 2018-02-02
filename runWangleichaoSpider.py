from scrapy import cmdline

# 免认证
cmdline.execute(['scrapy', 'crawl', 'FundNotice_PingAnDaHua', '-a', 'jobId=0L'])
# 自动登录

# Cookie认证




