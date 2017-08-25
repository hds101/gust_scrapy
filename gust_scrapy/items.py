# -*- coding: utf-8 -*-

from scrapy import Item, Field


class GustMaster(Item):
    company = Field()
    user = Field()


class GustCompany(Item):
    url = Field()
    name = Field()
    slogan = Field()
    overview = Field()
    industry = Field()
    location = Field()
    currency = Field()
    founded = Field()
    employees = Field()
    stage = Field()
    website = Field()
    incorporation_type = Field()


class GustUser(Item):
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
