import scrapy

class QuotesSpider(scrapy.Spider):
    name = "newegg"
    start_urls = ['https://www.newegg.com/Best-Selling-PCs-Monitors/EventSaleStore/ID-8722']

    def parse(self, response):
        for item in response.css('div.grid-col.radius-m.bg-white'):
            yield {
                'name': item.css('a.goods-title::text').get(),
                'price': str(item.css('span.goods-price-value strong::text').get()) + str(item.css('span.goods-price-value sup::text').get()),
                'og-price': str(item.css('div.goods-price-was.text-gray.font-s::text').get()).replace('$', ''),
                'rating': str(item.css('i.rating.rating-4-5::attr(aria-label)').get()).replace('rated', '').replace(' ', '').replace('outof', '/'),
                'rating-num': str(item.css('span.goods-rating-num.font-s.text-gray::text').get()).replace('(','').replace(')',''),
                'free-shipping': str(item.css('span.goods-price-ship-eligible.text-blue::text').get()).replace('Free Shipping','Yes')

                #'tags': quotes.css('a.tag::text').getall(),
            }
        #next_page = response.css('li.next a::attr(href)').get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)