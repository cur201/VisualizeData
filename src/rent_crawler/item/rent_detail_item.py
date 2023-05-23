import scrapy


class RentDetailItem(scrapy.Item):
    price = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    region = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    garage = scrapy.Field()
    type = scrapy.Field()
    pass
