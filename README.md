Install the following packages with pip:

    scrapy
    scrapy-rotating-proxies


Next, place a list of proxies  into the project's root directory. It should be named `proxies` and formatted as `https://IP:PORT`

Then run `scrapy crawl gust -o gust.json`
