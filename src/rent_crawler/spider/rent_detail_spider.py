import csv
import scrapy
import os
import pandas as pd
from src import get_element_selector, get_element_str, get_address, get_property_info, get_property_type


class RentDetailSpider(scrapy.Spider):
    name = "rent_detail"
    folder_name = "rent_detail"
    custom_settings = {
        'DETAIL_ITEM_PIPELINES': {
            'src.rent_crawler.DetailRentPipeline': 1
        }
    }

    def __init__(self, urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls

    def start_requests(self):
        for url in self._urls:
            yield scrapy.Request(url=url, callback=self.rent_detail_parse)

    def rent_detail_parse(self, response):
        self._response = response
        self._detail_process()
        # print(f'[{self.name}_PARSE]: {response}')

    def _detail_process(self):
        from src.rent_crawler import RentDetailItem
        detail_item = RentDetailItem()
        DIV_PROPERTY_SELECTOR = 'div[data-testid="listing-details__summary-left-column"]'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)

        detail_item['price'] = self._get_rent_price(property_selector)
        detail_item['addr'] = get_address(property_selector)
        detail_item['room'] = get_property_info(property_selector)
        detail_item['type'] = get_property_type(property_selector)

        self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'rent-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['price', 'address', 'room info', 'type'])

        data = {
            'price': [detail_item['price']],
            'addr': [detail_item['addr']],
            'room': [detail_item['room']],
            'type': [detail_item['type']]
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_rent_price(self, property_selector):
        rent_price = ''
        DIV_PRICE_SELECTOR = 'div[data-testid="listing-details__summary-title"]'
        div_selector = get_element_selector(property_selector, DIV_PRICE_SELECTOR)
        if len(div_selector) >= 1:
            rent_price = get_element_str(div_selector[0], "::text")
        else:
            rent_price = '-'
        print(f"Rent price: {rent_price}")
        return rent_price