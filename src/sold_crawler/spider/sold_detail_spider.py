import scrapy
from src import get_element_selector, get_element_str


class SoldDetailSpider(scrapy.Spider):
    name = 'sold_detail'
    folder_name = 'sold_detail'

    def __init__(self, urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls

    def start_requests(self):
        for url in self._urls:
            yield scrapy.Request(url=url, callback=self.sold_detail_parse)

    def sold_detail_parse(self, response):
        self._response = response
        self._detail_process()

    def _detail_process(self):
        print(f'sold item will be crawled here')