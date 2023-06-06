from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.sold_crawler import SoldDetailSpider


class SoldPipeline:
    def __init__(self):
        self._process = CrawlerProcess(settings=get_project_settings())
        self._queue = []

    def process_item(self, item, spider):
        urls = []
        addresses = []
        cities = []
        regions = []
        postcodes = []
        for element in item['soldList']:
            urls.append(element['url'])
            addresses.append(element['address'])
            cities.append(element['city'])
            regions.append(element['region'])
            postcodes.append(element['postcode'])

        return self._process.crawl(SoldDetailSpider, urls=urls, addresses=addresses, cities=cities, regions=regions)


