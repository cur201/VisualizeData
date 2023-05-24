import scrapy
import csv
import os
import pandas as pd
from src import get_element_selector, get_element_str, get_address, get_property_info, get_property_type, get_date_sold


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
        from src.sold_crawler import SoldDetailItem
        detail_item = SoldDetailItem()
        DIV_PROPERTY_SELECTOR = 'div[data-testid="listing-details__summary-left-column"]'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)

        detail_item['price'] = self._get_sold_price(property_selector)
        detail_item['addr'] = get_address(property_selector)
        detail_item['rooms'] = get_property_info(property_selector)
        detail_item['type'] = get_property_type(property_selector)
        detail_item['date_sold'] = get_date_sold(property_selector)

        self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'sold-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['price', 'address', 'room info', 'type', 'sold date'])

        data = {
            'price': [detail_item['price']],
            'addr': [detail_item['addr']],
            'rooms': [detail_item['rooms']],
            'type': [detail_item['type']],
            'date_sold': [detail_item['date_sold']]
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_sold_price(self, property_selector):
        sold_price = ''
        DIV_PRICE_SELECTOR = 'div[data-testid="listing-details__summary-title"]'
        div_selector = get_element_selector(property_selector, DIV_PRICE_SELECTOR)
        if len(div_selector) >= 1:
            sold_price = get_element_str(div_selector[0], "::text")
        else:
            sold_price = '-'
        print(f"Sold price: {sold_price}")
        return sold_price


