import scrapy


class komputronikScrapper(scrapy.Spider):
    name = 'komputronik'

    start_urls = [
        'https://www.komputronik.pl/category/1596/telefony,apple.html'
    ]

    custom_settings = {
        'COLLECTION_NAME': 'products'
    }

    def parse(self, response):
        for products in response.css('div.product-for-list'):
            yield {
                'name': products.css('div.pe2-head a::text').get().strip('\n').strip('\t'),
                'price': products.css('span.at-gross-price-0::text').get().strip('\n').strip('\t'),
                # 'category': products.css('p.product-category a::text').get().strip('\n').strip('\t'),
                'link': products.css('div.pe2-head a').attrib['href']
            }
