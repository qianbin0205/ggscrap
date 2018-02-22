from scrapy import cmdline

# 净值runFundNavSpider
# ---------------------------------------------------------------------------------------
# 杭州厚德载富财富
# cmdline.execute(['scrapy', 'crawl', 'FundNav_HoldGoodAsset', '-a', 'jobId=0L'])

# 海通资产
# cmdline.execute(['scrapy', 'crawl', 'FundNav_HaiTongAsset', '-a', 'jobId=0L'])

# 东海证券
# cmdline.execute(['scrapy', 'crawl', 'FundNav_DongHaiSecurities', '-a', 'jobId=0L'])

# 厦门致诚卓远投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_ZczyInvest', '-a', 'jobId=0L'])

# 季胜投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_JiShengInvest', '-a', 'jobId=0L'])

# 上海七曜投资
# cmdline.execute(['scrapy', 'crawl', 'FundNav_QiYaoInvest', '-a', 'jobId=0L'])

# 赤祺资产
cmdline.execute(['scrapy', 'crawl', 'FundNav_ChiQiFund', '-a', 'jobId=0L'])

#
# 公告runFundNoticeSpider
# ---------------------------------------------------------------------------------------
# 新世纪期货
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_NewCenturyFutures', '-a', 'jobId=0L'])

# 东吴证券
# cmdline.execute(['scrapy', 'crawl', 'FundNotice_DongWuSecurities', '-a', 'jobId=0L'])
