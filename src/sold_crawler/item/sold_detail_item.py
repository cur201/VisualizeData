import scrapy


class SoldDetailItem(scrapy.Item):
    addr = scrapy.Field()
    rooms = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    date_sold = scrapy.Field()
