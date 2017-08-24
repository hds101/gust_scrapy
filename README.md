Install the following packages with pip:

    pip install -r requirements.txt

Next, place a list of proxies into the project's root directory, it should be named `proxies` and formatted as `https://IP:PORT`. Or just run `scrapy crawl proxy`

Then run `scrapy crawl gust -o gust.json`
