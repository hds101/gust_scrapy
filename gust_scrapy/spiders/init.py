import os

from scrapy import FormRequest, Request, Spider
from scrapy.utils.spider import iterate_spider_output


class InitSpider(Spider):
    """Base Spider with initialization facilities"""
    login_page = 'https://gust.com/users/sign_in'

    def start_requests(self):
        self._postinit_reqs = super(InitSpider, self).start_requests()
        return iterate_spider_output(self.init_request())

    def initialized(self, response=None):
        """This method must be set as the callback of your last initialization
        request. See self.init_request() docstring for more info.
        """
        return self.__dict__.pop('_postinit_reqs')

    def init_request(self):
        """This function should return one initialization request, with the
        self.initialized method as callback. When the self.initialized method
        is called this spider is considered initialized. If you need to perform
        several requests for initializing your spider, you can do so by using
        different callbacks. The only requirement is that the final callback
        (of the last initialization request) must be self.initialized.
        The default implementation calls self.initialized immediately, and
        means that no initialization is needed. This method should be
        overridden only when you need to perform requests to initialize your
        spider
        """
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        return FormRequest.from_response(
            response,
            formxpath='//form[@action="/users/sign_in"]',
            formdata={
                'user[email]': os.environ['GUSTPARSER_EMAIL'],
                'user[password]': os.environ['GUSTPARSER_PASSWORD'],
                'user[remember_me]': '1',
            },
            callback=self.check_login_response,
        )

    def check_login_response(self, response):
        return self.initialized()
        # if "Brann's startup" in response.css('body').extract_first():
        #     self.log("Successfully logged in")
        #     self.initialized()
        # else:
        #     self.log("Login failed")
