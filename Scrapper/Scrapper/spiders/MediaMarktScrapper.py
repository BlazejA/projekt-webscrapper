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
            try:
                if products.css('div.old-price span::text').get() is not None:

                    old_price = products.css('div.old-price span::text').get().strip()
                else:
                     old_price = None

                yield {
                    'name': products.css('h2.title::text').get(),
                    'actual_price': products.css('span.whole::text').get().strip(),
                    'old_price': old_price,
                    'category': self.GetCategoryByProductName(products.css('h2.title::text').get()),
                    'shop': 'media_markt',
                    'details': {
                        'screen':
                            {
                                'screen_name': products.css('span.product-attribute-value::text').extract()[0:1][0].strip(),
                                'internal_storage': products.css('span.product-attribute-value::text').extract()[2:3][0].strip(),
                                'ram': products.css('span.product-attribute-value::text').extract()[3:4][0].strip(),
                                'camera': products.css('span.product-attribute-value::text').extract()[4:5][0].strip(),
                                'system': products.css('span.product-attribute-value::text').extract()[6:7][0].strip()
                            }
                    },
                    'img': products.css('div.column.gallery div.spark-image').attrib['src'],
                    'link': "https://mediamarkt.pl" + products.css('div.info a').attrib['href']
                }

                next_page = response.css('div.more-offers a').attrib['href']
                if next_page is not None:
                    yield response.follow("https://mediamarkt.pl"+next_page, callback=self.parse)

            except:
                if products.css('div.old-price span::text').get() is not None:

                    old_price = products.css('div.old-price span::text').get().strip()
                else:
                    old_price = None

                yield {
                    'name': products.css('h2.title::text').get(),
                    'actual_price': products.css('span.whole::text').get().strip(),
                    'old_price': old_price,
                    'category': self.GetCategoryByProductName(products.css('h2.title::text').get()),
                    'shop': 'media_markt',
                    'details': {
                        'screen':
                            {
                                'screen_name': products.css('span.product-attribute-value::text').extract()[0:1][0].strip(),
                                'internal_storage': products.css('span.product-attribute-value::text').extract()[2:3][
                                    0].strip(),
                                'ram': products.css('span.product-attribute-value::text').extract()[3:4][0].strip(),
                                'camera': products.css('span.product-attribute-value::text').extract()[4:5][0].strip(),
                                'system': None
                            }
                    },
                    'img': products.css('div.column.gallery div.spark-image').attrib['src'],
                    'link': "https://mediamarkt.pl" + products.css('div.info a').attrib['href']
                }

                next_page = response.css('div.more-offers a').attrib['href']
                if next_page is not None:
                    yield response.follow("https://mediamarkt.pl" + next_page, callback=self.parse)

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "Phone"
        elif "mac" in value.lower():
            return "Laptop"
        elif "ipad" in value.lower():
            return "Tablet"
        else:
            return "Other"
