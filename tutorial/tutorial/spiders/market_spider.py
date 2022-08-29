from urllib.request import Request
import scrapy
import cfscrape


class QuotesSpider(scrapy.Spider):
    name = "market"
    start_urls = ['https://journals.sagepub.com/doi/full/10.1177/00222437211073579']

    def start_requests(self):
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(url, 'Your prefarable user agent, _optional_')
            yield Request(url=url, cookies=token, headers={'User-Agent': agent})

    def parse(self, response):
        yield {
            'name': response.css('div.publicationContentTitle').get(),
        }
