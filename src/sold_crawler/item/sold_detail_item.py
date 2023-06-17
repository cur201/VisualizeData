import scrapy


class SoldDetailItem(scrapy.Item):
    price = scrapy.Field()
    municipality = scrapy.Field()
    sold_date = scrapy.Field()
    property_type = scrapy.Field()
    bedroom = scrapy.Field()
    bathroom = scrapy.Field()
    area = scrapy.Field()
    year_built = scrapy.Field()
    neighborhood_median_price = scrapy.Field()
    compared_to_nearby_properties = scrapy.Field()

