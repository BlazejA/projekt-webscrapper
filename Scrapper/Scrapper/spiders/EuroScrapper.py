import unicodedata

import scrapy


class EuroScrapper(scrapy.Spider):
    name = 'euro'

    page = 2
    start_urls = [
        'https://www.euro.com.pl/telefony-komorkowe,_Apple.bhtml'
    ]

    custom_settings = {
        'Scrapper.pipelines.ScrapperPipeline': 300,
    }

    def GetCategoryByProductName(self, value: str) -> str:
        if "iphone" in value.lower():
            return "smartphone"
        elif "mac" in value.lower():
            return "laptop"
        else:
            return "other"

    def CastDataNames(self, values):
        newDict = {}
        for item in values:
            if item == "Wyświetlacz":
                newDict["screen"] = values["Wyświetlacz"]
            elif item == "Aparaty tylny/przedni":
                newDict["camera"] = values["Aparaty tylny/przedni"]
            elif item == "System operacyjny":
                newDict["system"] = values["System operacyjny"]
            elif item == "Pamięć":
                mem = values["Pamięć"].split("/ ")
                newDict["ram"] = mem[0][:-1]
                newDict["internalStorage"] = mem[1]
            elif item == "Procesor":
                newDict["procesor"] = values["Procesor"]
        return newDict

    def parse(self, response):
        for products in response.css('div.product-for-list'):
            try:
                item1 = products.css('div.attributes-row  span::text, div.attributes-row a::text').getall()
                item = [i.strip() for i in item1 if i.strip()]
                dict = {item[i]: item[i + 1].strip() for i in range(0, len(item), 2)}
                newDict = self.CastDataNames(dict)
                yield {
                    'name': products.css('h2.product-name a::text').get().strip(),
                    'actualPrice': products.css('div.price-normal::text').get().strip("zł").strip().replace(u'\xa0', u''),
                    'oldPrice': products.css('div.price-old::text').get().strip("zł").strip().replace(u'\xa0', u''),
                    'category': self.GetCategoryByProductName(products.css('h2.product-name a::text').get().strip()),
                    'link': "https://www.euro.com.pl" + products.css('h2.product-name a').attrib['href'],
                    'shop': 'rtv_euro_agd',
                    'img': products.css('a.photo-hover img::attr(data-original)').get(),
                    'details': {
                        item: newDict.get(item) for item in newDict
                    }
                }
            except:
                item1 = products.css('div.attributes-row  span::text, div.attributes-row a::text').getall()
                item = [i.strip() for i in item1 if i.strip()]
                dict = {item[i]: item[i + 1].strip() for i in range(0, len(item), 2)}
                newDict = self.CastDataNames(dict)
                yield {
                    'name': products.css('h2.product-name a::text').get().strip(),
                    'actualPrice': products.css('div.price-normal::text').get().strip("zł").strip().replace(u'\xa0', u''),
                    'oldPrice': "",
                    'category': self.GetCategoryByProductName(products.css('h2.product-name a::text').get().strip()),
                    'link': "https://www.euro.com.pl" + products.css('h2.product-name a').attrib['href'],
                    'shop': 'rtv_euro_agd',
                    'img': products.css('a.photo-hover img::attr(data-original)').get(),
                    'details': {
                        item: newDict.get(item) for item in newDict
                    }
                }

        next_page = "https://www.euro.com.pl/telefony-komorkowe,_Apple,strona-" + str(self.page) + ".bhtml"

        numbers_list = [int(x.strip()) for x in response.css("div.paging-numbers a::text").extract()]
        page_number = max(numbers_list)

        if self.page <= page_number:
            try:
                yield response.follow(next_page, callback=self.parse)
                self.page += 1
            except:
                return
        else:
            scrapy.Spider.close(self, reason="Cannot find url")
