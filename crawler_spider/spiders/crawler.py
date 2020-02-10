# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from twisted.internet.error import DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CrawlerSpider(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['xyz.com']
    start_urls = ['http://xyz.com/']

    handle_httpstatus_list = [403, 404]

    rules = (Rule(LinkExtractor(), callback='parse_page', follow=True),)

    def parse_page(self, response):
        yield {'response_status': response.status,
               'response_url': response.url}

    def parse_failed_domain(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            yield {'response_status': response.status,
                   'response_url': response.url}

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            yield {'response_status': response.status,
                   'response_url': response.url}

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            yield {'response_status': response.status,
                   'response_url': response.url}
