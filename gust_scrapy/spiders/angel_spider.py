# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request
from scrapy.shell import inspect_response


class AngelSpider(Spider):
    name = 'angel'

    def start_requests(self):
        yield Request(
            method='GET',
            url='https://angel.co/job_listings/startup_ids?' \
                '&filter_data[salary][min]=0&' \
                '&filter_data[salary][max]=2000&' \
                '&filter_data[types][]=full-time' \
                '&tab=find',
            callback=self.parse
        )

    def parse(self, response):
        inspect_response(response, self)
