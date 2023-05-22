import scrapy


class RentDetailItem(scrapy.Item):
    price = scrapy.Field()
    addr = scrapy.Field()
    room = scrapy.Field()
    type = scrapy.Field()
    pass
