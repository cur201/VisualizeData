import csv
import scrapy
import os
import pandas as pd
import re
from src import get_element_selector, get_element_str


class RentDetailSpider(scrapy.Spider):
    name = "rent_detail"
    folder_name = "rent_detail"
    custom_settings = {
        'DETAIL_ITEM_PIPELINES': {
            'src.rent_crawler.DetailRentPipeline': 2
        }
    }

    def __init__(self, urls, municipalities, rental_types, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls
        self._municipalities = municipalities
        self._rental_types = rental_types

    def start_requests(self):
        print(len(self._urls), len(self._municipalities), len(self._rental_types))
        for i in range(len(self._urls)):
            url = self._urls[i]
            municipality = self._municipalities[i]
            rental_type = self._rental_types[i]
            yield scrapy.Request(url=url, callback=self.rent_detail_parse,
                                 cb_kwargs=dict(municipality=municipality, rental_type=rental_type))

    def rent_detail_parse(self, response, municipality, rental_type):
        self._response = response
        self._detail_process(municipality, rental_type)

    def _detail_process(self, municipality, rental_type):
        pass



