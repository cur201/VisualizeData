import scrapy


class SoldDetailItem(scrapy.Item):
    address = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    garage = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    date_sold = scrapy.Field()
