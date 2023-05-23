from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings

class DetailRentPipeline:
    def __init__(self):
        self._process = CrawlerProcess(settings=get_project_settings())
        self._queue = []

    def process_item(self, detail_item, spider):
        pass