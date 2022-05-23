import scrapy


class MediaScrapper(scrapy.Spider):
    name = 'MediaMarkt'

    start_urls = [
        'https://mediamarkt.pl/telefony-i-smartfony/smartfony/wszystkie-smartfony.apple'
    ]

    custom_settings = {
        'COLLECTION_NAME': 'products'
    }

    def parse(self, response):
        for products in response.css('div.list'):
            yield {
                'name': products.css('h2.title a::text').get().strip('\n').strip('\t'),
                'price': products.css('span.whole::text').get().strip('\n').strip('\t'),
                #'category': products.css('p.product-category a::text').get().strip('\n').strip('\t'),
                'link': products.css('h2.title a').attrib['href']
            }

