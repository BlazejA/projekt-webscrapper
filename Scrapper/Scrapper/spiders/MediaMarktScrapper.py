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
                'price': products.css('span.whole::text').get().strip(),
                'category': self.GetCategoryByProductName(products.css('h2.title::text').get()),
                'link': products.css('div.info a').attrib['href']
            }


        next_page = response.css('div.more-offers a').attrib['href']
        if next_page is not None:
            yield response.follow("https://mediamarkt.pl"+next_page, callback=self.parse)

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "Phone"
        elif "mac" in value.lower():
            return "Laptop"
        elif "ipad" in value.lower():
            return "Tablet"
        else:
            return "Other"
