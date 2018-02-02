# -*- coding: utf-8 -*-

from .XinPiBao import XinPiBaoSpider


class BJTHCapitalSpider(XinPiBaoSpider):
    name = 'FundNav_BJTHCapital'
    sitename = '天和思创投资'
    channel = '投资顾问'

    org_id = 'M12043'

    def __init__(self, limit=None, *args, **kwargs):
        super(BJTHCapitalSpider, self).__init__(limit, *args, **kwargs)
