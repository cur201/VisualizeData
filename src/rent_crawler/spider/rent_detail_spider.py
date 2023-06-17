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
        from src.rent_crawler import RentDetailItem
        detail_item = RentDetailItem()
        DIV_PROPERTY_SELECTOR = 'div.sc-jgbSNz'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)[0]
        print(property_selector)
        property_info = self._get_property_info(property_selector)
        price = self._get_property_price(property_selector)
        bedroom, bathroom, area = property_info
        print("municipality =", municipality, 'rental_type =', rental_type, 'price =', price, 'bedroom =', bedroom, 'bathroom =', bathroom, 'area =', area)
        detail_item['price'] = price
        detail_item['municipality'] = municipality
        detail_item['rental_type'] = rental_type
        detail_item['bedroom'] = bedroom
        detail_item['bathroom'] = bathroom
        detail_item['area'] = area

        self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'rent-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['price', 'municipality', 'rental_type', 'bedroom', 'bathroom', 'area'])

        data = {
            'price': [detail_item['price']],
            'municipality': [detail_item['municipality']],
            'rental_type': [detail_item['rental_type']],
            'bedroom': [detail_item['bedroom']],
            'bathroom': [detail_item['bathroom']],
            'area': [detail_item['area']]
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_property_price(self, property_selector):
        PRICE_SELECTOR = 'div.Price__Component-rui__x3geed-0.hAEpgA.heading'
        price = get_element_selector(property_selector, PRICE_SELECTOR)
        return get_element_str(price, '::text')

    def _get_property_info(self, property_selector):
        INFO_SELECTOR = 'div.overview.overview-component-bed-bath-sqft'
        LI_BED_SELECTOR = 'li[data-testid="property-meta-beds"] > span[data-testid="meta-value"]'
        LI_BATH_SELECTOR = 'li[data-testid="property-meta-baths"] > span[data-testid="meta-value"]'
        LI_AREA_SELECTOR = 'li[data-testid="property-meta-sqft"]'

        info = get_element_selector(property_selector, INFO_SELECTOR)
        li_bed = get_element_selector(info, LI_BED_SELECTOR)
        li_bath = get_element_selector(info, LI_BATH_SELECTOR)
        li_area = get_element_selector(info, LI_AREA_SELECTOR)

        bedroom = get_element_str(li_bed, '::text') if len(li_bed) else '-'
        bathroom = get_element_str(li_bath, '::text') if len(li_bath) else '-'
        area = get_element_str(li_area, '::text') if len(li_area) else '-'
        return bedroom, bathroom, area
