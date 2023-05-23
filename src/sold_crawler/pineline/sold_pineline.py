from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.sold_crawler import SoldDetailSpider


class SoldPipeline:
    def __init__(self):
        self._process = CrawlerProcess(settings=get_project_settings())
        self._queue = []

    def process_item(self, item, spider):
        urls = []
        for element in item['soldList']:
            urls.append(element['url'])

        return self._process.crawl(SoldDetailSpider, urls=urls)


