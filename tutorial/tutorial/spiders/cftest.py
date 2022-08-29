import scrapy


class DataSpider(scrapy.Spider):
    name = "avvo"

    def start_requests(self):
        urls = [
            'https://www.avvo.com/attorneys/84025-ut-jason-hunter-284784/reviews.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self):
        self.called = False

        self.data = {}

    def parse(self, response):
        if not self.called:
            self.called = True

            self.data["website"] = response.css('title::text').get()

            yield self.data