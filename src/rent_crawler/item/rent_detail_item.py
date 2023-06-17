import scrapy


class RentDetailItem(scrapy.Item):
    price = scrapy.Field()
    municipality = scrapy.Field()
    rental_type = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    area = scrapy.Field()
    pass
