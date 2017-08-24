# -*- coding: utf-8 -*-

import os

from scrapy import Spider

class ProxySpider(Spider):
    name = 'proxy'
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
    }
    start_urls = [
        'https://www.sslproxies.org/'
    ]

    def parse(self, response):
        os.remove('proxies')
        for row in response.css('table.table tbody tr'):
            ip = row.css('td:nth-child(1)::text').extract_first()
            port = row.css('td:nth-child(2)::text').extract_first()
            proxy = "https://{ip}:{port}\n".format(ip=ip, port=port)
            print(proxy)
            with open('proxies', 'a') as f:
                f.write(proxy)
