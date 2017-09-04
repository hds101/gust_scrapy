# -*- coding: utf-8 -*-

import os
from scrapy import Spider


class ProxySpider(Spider):
    name = 'proxy'
    custom_settings = { 'DOWNLOADER_MIDDLEWARES': {} }

    start_urls = [
        'https://www.sslproxies.org/'
    ]

    def parse(self, response):
        try:
            os.remove('proxies')
        except FileNotFoundError:
            pass

        for row in response.css('table.table tbody tr'):
            ip = row.css('td:nth-child(1)::text').extract_first()
            port = row.css('td:nth-child(2)::text').extract_first()
            with open('proxies', 'a') as f:
                f.write("https://{ip}:{port}\n".format(ip=ip, port=port))
