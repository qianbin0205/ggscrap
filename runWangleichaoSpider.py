from scrapy import cmdline

# 免认证
#上海厚崇资产-投资顾问
cmdline.execute(['scrapy', 'crawl', 'FundNotice_PingAnDaHua', '-a', 'jobId=0L'])
cmdline.execute(['scrapy', 'crawl', 'FundNotice_PingAnDaHua', '-a', 'jobId=0L'])
#中邮证券-券商资管净值
cmdline.execute(['scrapy', 'crawl', 'FundNav_zystock', '-a', 'jobId=0L'])
#渤海证券-券商资管净值
cmdline.execute(['scrapy', 'crawl', 'FundNav_bhhjamc', '-a', 'jobId=0L'])
# 自动登录
#浙江慧安家族财富投资-投资顾问
cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhejiangHuian', '-a', 'jobId=0L'])
#中域投资-投资顾问
cmdline.execute(['scrapy', 'crawl', 'FundNav_ZhongyuInvset', '-a', 'jobId=0L'])
#蓝海韬略-投资顾问
cmdline.execute(['scrapy', 'crawl', 'FundNav_LanhaiTaolue', '-a', 'jobId=0L'])
# Cookie认证




