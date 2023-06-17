from scrapy.crawler import CrawlerRunner, CrawlerProcess
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
        municipalities = []
        rental_types = []

        for element in item['list']:
            urls.append(element['url'])
            municipalities.append(element['municipality'])
            rental_types.append(element['rental_type'])

        return self._process.crawl(RentDetailSpider, urls=urls, municipalities=municipalities, rental_types=rental_types)
    