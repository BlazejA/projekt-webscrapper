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


        for products in response.css('div.offer'):

            yield {
                'name': products.css('h2.title::text').get(),
                'price': products.css('span.whole::text').get().strip('\n    ').strip('\n  '),
                'category': self.GetCategoryByProductName(products.css('h2.title::text').get()),
                'link': products.css('div.info a').attrib['href']
            }

    def GetCategoryByProductName(self,value: str) -> str:
        if "iphone" in value.lower():
            return "Phone"
        elif "mac" in value.lower():
            return "Laptop"
        elif "ipad" in value.lower():
            return "Tablet"
        else:
            return "Other"