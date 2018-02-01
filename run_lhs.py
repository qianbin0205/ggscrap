from scrapy import cmdline

#第一创业证券资管
#cmdline.execute(['scrapy', 'crawl', 'FundNav_DiyichuangyeSecuritiesManagement', '-a', 'jobId=0L'])

#中粮期货
cmdline.execute(['scrapy', 'crawl', 'FundNotice_Zlqh', '-a', 'jobId=0L'])
