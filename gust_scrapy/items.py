# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GustCompany(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    slogan = scrapy.Field()
    overview = scrapy.Field()
    data = scrapy.Field()

class GustUser(scrapy.Item):
    pass
