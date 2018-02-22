from scrapy import Item, Field


# 基础Item
class GGItem(Item):
    hkey = Field()  # 哈希主键

    groupname = Field()  # 分组名称
    sitename = Field()  # 站点名称
    channel = Field()  # 频道名称
    entry = Field()  # 频道入口
