import scrapy
from gust_scrapy.items import GustCompany, GustUser


class GustSpider(scrapy.Spider):
    name = 'gust'
    start_urls = [
        'https://gust.com/search/new?category=startups&page=1&partial=results',
    ]

    def parse(self, response):
        for href in response.css('.card-title > a::attr(href)'):
            yield response.follow(href, self.parse_company)

        stop_on = 3
        next_page = response.css('ul.pagination li.last')[0].css('a::attr(href)').extract_first()
        if (next_page != ('/search/new?category=startups&page=%s&partial=results' % stop_on)) and next_page is not None:
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
        company['name'] = response.css('#company_info h2::text').extract_first().strip()
        company['slogan'] = response.css('#company_info p.quote::text').extract_first().strip()
        company['overview'] = response.css('#company_overview .panel-body > p::text').extract_first().strip()
        company['data'] = dynamic_fields

        yield company

    def parse_user(self, response):
        return None
