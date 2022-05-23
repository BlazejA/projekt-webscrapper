import scrapy


class EuroScrapper(scrapy.Spider):
    name = 'euro'

    start_urls = [
        'https://www.euro.com.pl/telefony-komorkowe,_Apple.bhtml'
    ]

    custom_settings = {
        'COLLECTION_NAME': 'products'
    }

    def parse(self, response):
        for products in response.css('div.product-for-list'):
            yield {
                'name': products.css('h2.product-name a::text').get().strip('\n').strip('\t'),
                'price': products.css('div.price-normal::text').get().strip('\n').strip('\t'),
                'category': products.css('p.product-category a::text').get().strip('\n').strip('\t'),
                'brand': products.css('a.product-brand::text').get().strip('\n').strip('\t'),
                'link': products.css('h2.product-name a').attrib['href']
            }
