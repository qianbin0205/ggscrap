SPIDER_MODULES = ['FundNavSpiders', 'FundNoticeSpiders']

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}

proxy = 'http://111.13.111.184:80'
anonymous_proxy = 'http://114.215.95.188:3128'

fund_nav = {
    'db': {
        'host': '192.168.0.53',
        'name': 'scrapy_debug_db',
        'port': 1433,
        'user': 'sql_scrapy',
        'pswd': 'sql_scrapy123',
        'table': 't_nav_general',
        'timeout': 60
    }
}

fund_notice = {
    'db': {
        'host': '192.168.0.53',
        'name': 'scrapy_debug_db',
        'port': 1433,
        'user': 'sql_scrapy',
        'pswd': 'sql_scrapy123',
        'table': 't_fund_announcement',
        'timeout': 60
    }
}
