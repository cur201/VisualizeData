﻿from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from src.rent_crawler import RentDetailSpider
from time import sleep
from twisted.internet.asyncioreactor import AsyncioSelectorReactor as reactor


class RentPipeline:
    def __init__(self):
        self._process = CrawlerProcess(settings=get_project_settings())
        self._queue = []

    def process_item(self, item, spider):
        urls = []
        addresses = []
        cities = []
        regions = []
        postcodes = []
        for element in item['list']:
            urls.append(element['url'])
            addresses.append(element['address'])
            cities.append(element['city'])
            regions.append(element['region'])
            postcodes.append(element['postcode'])

        return self._process.crawl(RentDetailSpider, urls=urls, addresses=addresses, cities=cities, regions=regions, postcodes=postcodes)
    