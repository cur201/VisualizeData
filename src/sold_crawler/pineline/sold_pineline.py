from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.sold_crawler import SoldDetailSpider


class SoldPipeline:
    def __init__(self):
        self._process = CrawlerProcess(settings=get_project_settings())
        self._queue = []

    def process_item(self, item, spider):
        urls = []
        sold_dates = []

        for element in item['soldList']:
            urls.append(element['url'])
            sold_dates.append(element['sold_date'])

        return self._process.crawl(SoldDetailSpider, urls=urls, sold_dates=sold_dates)


