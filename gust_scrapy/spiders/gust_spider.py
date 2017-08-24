# -*- coding: utf-8 -*-

import re
from scrapy import Request
from gust_scrapy.spiders.init import InitSpider
from gust_scrapy.items import GustCompany, GustUser


class GustSpider(InitSpider):
    name = 'gust'

    def __init__(self, start_at=1, stop_at=3, *args, **kwargs):
        super(GustSpider, self).__init__(*args, **kwargs)
        self.start_at = start_at
        self.start_urls = [
            "https://gust.com/search/new?category=startups&page={start_at}&partial=results".format(start_at=start_at)
        ]
        self.stop_at = "/search/new?category=startups&page={stop_at}&partial=results".format(stop_at=(int(stop_at) + 1))

    def parse(self, response):
        for href in response.css('.card-title > a::attr(href)'):
            yield response.follow(href, self.parse_company)

        next_page = response.css('ul.pagination li.last')[0].css('a::attr(href)').extract_first()
        if (next_page != self.stop_at) and next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_company(self, response):
        company = GustCompany()
        dynamic_fields = dict()
        for item in response.css('#company_info ul.list-group li.list-group-item'):

            key = item.css('::text').extract_first().split()[0].lower().strip()
            value = item.css('span.value::text').extract_first().strip()

            if key == 'website':
                value = item.css('span.value a::attr(href)').extract_first().strip()
            elif key == 'incorporation':
                key = 'incorporation_type'

            dynamic_fields[key] = value

        company['url'] = response.url
        company['name'] = self.__extract(response, '#company_info h2::text')
        company['slogan'] = self.__extract(response, '#company_info p.quote::text')
        company['overview'] = self.__extract(response, '#company_overview .panel-body > p::text')
        company['data'] = dynamic_fields

        for user in response.css('#startup_content > .panel #management .card-title a::attr(href)'):
            yield response.follow(user, callback=self.parse_user, meta={'company': dict(company), 'tag': 'Team'})

        for user in response.css('#startup_content > .panel #advisors .card-title a::attr(href)'):
            yield response.follow(user, callback=self.parse_user, meta={'company': dict(company), 'tag': 'Advisors'})

        for user in response.css('#startup_content > .panel #investor .card-title a::attr(href)'):
            yield response.follow(user, callback=self.parse_user, meta={'company': dict(company), 'tag': 'Previous Investors'})

    def parse_user(self, response):
        user = GustUser()

        user['company'] = response.meta['company']
        user['tag'] = response.meta['tag']
        user['url'] = response.url

        user['name'] = self.__extract(response, '#user_profile .profile .card-title::text')
        user['location'] = self.__extract(response, '#user_profile .profile .card-subtitle > div > span::text')
        user['role'] = self.__extract(response, '#user_profile .profile .card-subtitle > p::text')
        user['website'] = self.__extract(response, '#contact_info .list-group-item:nth-child(1) .value a::attr(href)')

        try:
            bio = ' '.join(response.css('#user_profile #biography .value .rest .active.hidden p::text').extract())
            user['biography'] = re.sub(r'Show\sLess$', '', bio).strip()
        except NoneType:
            user['biography'] = None

        user['social_linkedin'] = None
        user['social_twitter'] = None
        user['social_facebook'] = None
        social_links = response.css('#contact_info .list-group-item:nth-child(2) .value a::attr(href)').extract()
        if social_links is not None:
            for link in social_links:
                if link is not None and 'linkedin.com' in link:
                    user['social_linkedin'] = link.strip()
                elif link is not None and 'twitter.com' in link:
                    user['social_twitter'] = link.strip()
                elif link is not None and 'facebook.com' in link:
                    user['social_facebook'] = link.strip()

        yield user

    def __extract(self, response, selector):
        try:
            return response.css(selector).extract_first().strip()
        except AttributeError:
            return None
