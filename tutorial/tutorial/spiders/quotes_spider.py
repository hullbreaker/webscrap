import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['https://quotes.toscrape.com/']

    def parse(self, response):
        for quotes in response.css('div.quote'):
            yield {
                'name': quotes.css('span.text::text').get().replace('“', '').replace('”', ''),
                'author': quotes.css('small.author::text').get(),
                'tags': quotes.css('a.tag::text').getall(),
            }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)