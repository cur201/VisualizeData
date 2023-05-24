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
            'src.rent_crawler.DetailRentPipeline': 2
        }
    }

    def __init__(self, urls, addresses, cities, regions, postcodes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls
        self._addresses = addresses
        self._cities = cities
        self._regions = regions
        self._postcodes = postcodes

    def start_requests(self):
        for i in range(len(self._urls)):
            url = self._urls[i]
            address = self._addresses[i]
            city = self._cities[i]
            region = self._regions[i]
            yield scrapy.Request(url=url, callback=self.rent_detail_parse,
                                 cb_kwargs=dict(address=address, city=city, region=region))

    def rent_detail_parse(self, response, address, city, region):
        self._response = response
        self._detail_process(address, city, region)
        print(f'[{self.name}_PARSE]: {response}')

    def _detail_process(self, address, city, region):
        from src.rent_crawler import RentDetailItem
        detail_item = RentDetailItem()
        DIV_PROPERTY_SELECTOR = 'div[data-testid="listing-details__summary-left-column"]'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)

        detail_item['address'] = address
        detail_item['city'] = city
        detail_item['region'] = region
        detail_item['type'] = get_property_type(property_selector)
        property_info = get_property_info(property_selector)
        price = self._get_rent_price(property_selector)
        if len(property_info) > 0 and price > 0:
            bedroom, bathroom, garage = property_info
            detail_item['bedroom'] = '1' if bedroom == '−' else bedroom
            detail_item['bathroom'] = '1' if bathroom == '−' else bathroom
            detail_item['garage'] = '1' if garage == '−' else garage
            detail_item['price'] = price
            self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'rent-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['price', 'address', 'city ', 'region', 'postcode', 'bedroom', 'bathroom', 'garage', 'type'])

        data = {
            'price': [detail_item['price']],
            'address': [detail_item['address']],
            'city': [detail_item['city']],
            'region': [detail_item['region']],
            'bedroom': [detail_item['bedroom']],
            'bathroom': [detail_item['bathroom']],
            'garage': [detail_item['garage']],
            'type': [detail_item['type']]
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_rent_price(self, property_selector):
        rent_price = ''
        DIV_PRICE_SELECTOR = 'div[data-testid="listing-details__summary-title"]'
        div_selector = get_element_selector(property_selector, DIV_PRICE_SELECTOR)
        if len(div_selector) >= 1:
            rent_price = get_element_str(div_selector[0], "::text").split(' ')[0].replace("$", "").replace(",", "").split('.')[0]
        else:
            rent_price = '-'
        print(f"Rent price: {rent_price}")
        if rent_price == 'Leased':
            return 0
        else:
            return int(rent_price)
