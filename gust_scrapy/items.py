# -*- coding: utf-8 -*-

from scrapy import Item, Field


class GustCompany(Item):
    url = Field()
    name = Field()
    slogan = Field()
    overview = Field()
    data = Field()

class GustUser(Item):
    company = Field()
    tag = Field()
    url = Field()
    name = Field()
    location = Field()
    role = Field()
    biography = Field()
    website = Field()
    social_linkedin = Field()
    social_twitter = Field()
    social_facebook = Field()
