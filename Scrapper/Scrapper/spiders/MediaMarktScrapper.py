import scrapy


class MediaScrapper(scrapy.Spider):
    name = 'MediaMarkt'

    start_urls = [
        'https://mediamarkt.pl/telefony-i-smartfony/smartfony/wszystkie-smartfony.apple',
        'https://mediamarkt.pl/komputery-i-tablety/laptopy-laptopy-2-w-1/notebooki.apple',
    ]

    custom_settings = {
        'Scrapper.MediaMarktPipelines.ScrapperPipeline': 400,
    }

    global count
    count = 0

    def parse(self, response):

        for products in response.css('div.offer'):
            global count
            count += 1
            if products.css('div.old-price span::text').get() is not None:

                old_price = products.css('div.old-price span::text').get().strip()
            else:
                old_price = None
            try:
                actual_price = products.css('span.whole::text').get().strip()
            except:
                actual_price = None

            try:
                system = products.css('span.product-attribute-value::text').extract()[6:7][0].strip()
            except:
                system = None

            try:
                screen = products.css('span.product-attribute-value::text').extract()[0:1][0].strip()
            except:
                screen = None

            try:
                internal_storage = products.css('span.product-attribute-value::text').extract()[2:3][0].strip()
            except:
                internal_storage = None

            try:
                ram = products.css('span.product-attribute-value::text').extract()[3:4][0].strip()
            except:
                ram = None

            try:
                camera = products.css('span.product-attribute-value::text').extract()[4:5][0].strip()
            except:
                camera = None
            yield {
                'name': products.css('h2.title::text').get(),
                'actualPrice': actual_price,
                'oldPrice': old_price,
                'category': self.GetCategoryByProductName(products.css('h2.title::text').get()),
                'shop': 'media_markt',
                'details': {
                    'screen': screen,
                    'internalStorage': internal_storage,
                    'ram': ram,
                    'camera': camera,
                    'system': system

                },
                'img': products.css('div.column.gallery div.spark-image').attrib['src'],
                'link': "https://mediamarkt.pl" + products.css('div.info a').attrib['href']
            }

        next_page = response.css('div.more-offers a').attrib['href']
        if count >= 130:
            scrapy.Spider.close(self, reason="end")

        elif next_page is not None:
            yield response.follow("https://mediamarkt.pl" + next_page, callback=self.parse)

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "smartphone"
        elif "mac" in value.lower():
            return "laptop"
        else:
            return "other"
