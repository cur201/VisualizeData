import scrapy
import csv
import os
import pandas as pd
from src import get_element_selector, get_element_str, get_address, get_property_info, get_property_type, get_date_sold


class SoldDetailSpider(scrapy.Spider):
    name = 'sold_detail'
    folder_name = 'sold_detail'

    def __init__(self, urls, addresses, cities, regions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls
        self._addresses = addresses
        self._cities = cities
        self._regions = regions

    def start_requests(self):
        for i in range(len(self._urls)):
            url = self._urls[i]
            address = self._addresses[i]
            city = self._cities[i]
            region = self._regions[i]
            yield scrapy.Request(url=url, callback=self.sold_detail_parse,
                                 cb_kwargs=dict(address=address, city=city, region=region))

    def sold_detail_parse(self, response, address, city, region):
        self._response = response
        self._detail_process(address, city, region)

    def _detail_process(self, address, city, region):
        from src.sold_crawler import SoldDetailItem
        detail_item = SoldDetailItem()
        DIV_PROPERTY_SELECTOR = 'div[data-testid="listing-details__summary-left-column"]'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)

        price = self._get_sold_price(property_selector)
        detail_item['address'] = address
        detail_item['city'] = city
        detail_item['region'] = region
        detail_item['type'] = get_property_type(property_selector)
        detail_item['date_sold'] = get_date_sold(property_selector)
        property_info = get_property_info(property_selector)
        if len(property_info) > 0:
            if len(property_info) == 3:
                bedroom, bathroom, garage = property_info
            else:
                bedroom, bathroom, garage = '-', '-', '-'
            detail_item['bedroom'] = bedroom
            detail_item['bathroom'] = bathroom
            detail_item['garage'] = garage
            detail_item['price'] = price
        self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'sold-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['price', 'address', 'city ', 'region', 'bedroom', 'bathroom', 'garage', 'type',
                                 'sold date'])

        data = {
            'price': [detail_item['price']],
            'address': [detail_item['address']],
            'city': [detail_item['city']],
            'region': [detail_item['region']],
            'bedroom': [detail_item['bedroom']],
            'bathroom': [detail_item['bathroom']],
            'garage': [detail_item['garage']],
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


