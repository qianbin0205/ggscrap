# -*- coding: utf-8 -*-

from .XinPiBao import XinPiBaoSpider


class XinPuAssetSpider(XinPiBaoSpider):
    name = 'FundNav_XinPuAsset'
    sitename = '信普资产'
    channel = '投顾净值'

    org_id = 'M11451'

    def __init__(self, limit=None, *args, **kwargs):
        super(XinPuAssetSpider, self).__init__(limit, *args, **kwargs)
