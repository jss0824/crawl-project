# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# hellow

class BaiduNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    TITLE = scrapy.Field()
    AUTHOR = scrapy.Field()
    PUBTIME = scrapy.Field()
    URL = scrapy.Field()
    SOURCE = scrapy.Field()
    INSERTTIME = scrapy.Field()
    MD5 = scrapy.Field()
    CONTENT = scrapy.Field()
    BRIEF = scrapy.Field()
    IMG_URL = scrapy.Field()
    Category = scrapy.Field()
    htmlContent = scrapy.Field()
    insertTime = scrapy.Field()
    SEARCH_KEYWORD = scrapy.Field()
    pass
