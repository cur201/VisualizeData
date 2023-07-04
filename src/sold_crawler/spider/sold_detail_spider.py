import time

import scrapy
import csv
import os
import pandas as pd
from src import get_element_selector, get_element_str


class SoldDetailSpider(scrapy.Spider):
    name = 'sold_detail'
    folder_name = 'sold_detail'

    def __init__(self, urls, sold_dates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None
        self._urls = urls
        self._sold_dates = sold_dates

    def start_requests(self):
        for i in range(len(self._urls)):
            url = self._urls[i]
            sold_date = self._sold_dates[i]
            time.sleep(10)
            yield scrapy.Request(url=url, callback=self.sold_detail_parse,
                                 cb_kwargs=dict(sold_date=sold_date))

    def sold_detail_parse(self, response, sold_date):
        self._response = response
        self._detail_process(sold_date)

    def _detail_process(self, sold_date):
        from src.sold_crawler import SoldDetailItem
        detail_item = SoldDetailItem()

        DIV_PROPERTY_PRICE = 'div[data-testid="last-sold-container"]'
        div_price = get_element_selector(self._response, DIV_PROPERTY_PRICE)
        DIV_PROPERTY_FACT = 'div[data-testid="pdp-home-facts"]'
        div_property_fact = get_element_selector(self._response, DIV_PROPERTY_FACT)
        DIV_PROPERTY_INFO = 'ul[data-testid="pdp-highlighted-facts"]'
        div_property_info = get_element_selector(self._response, DIV_PROPERTY_INFO)
        price = self._get_property_price(div_price)
        municipality = self._get_sold_municipality(div_property_fact)
        bedroom, bathroom, area = self._get_property_info(div_property_fact)
        property_type, year_build = self._get_property_features(div_property_info)
        compare, median = self._get_compare_median(self._response)
        detail_item['price'] = price
        detail_item['municipality'] = municipality
        detail_item['sold_date'] = sold_date
        detail_item['property_type'] = property_type
        detail_item['bedroom'] = bedroom
        detail_item['bathroom'] = bathroom
        detail_item['area'] = area
        detail_item['year_built'] = year_build
        detail_item['neighborhood_median_price'] = median
        detail_item['compared_to_nearby_properties'] = compare
        self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'sold-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['price', 'municipality', 'sold_date', 'property_type', 'bedroom', 'bathroom', 'area',
                                 'year_built', 'neighborhood_median_price', 'compared_to_nearby_properties'])

        data = {
            'price': [detail_item['price']],
            'municipality': [detail_item['municipality']],
            'sold_date': [detail_item['sold_date']],
            'property_type': [detail_item['property_type']],
            'bedroom': [detail_item['bedroom']],
            'bathroom': [detail_item['bathroom']],
            'area': [detail_item['area']],
            'year_built': [detail_item['year_built']],
            'neighborhood_median_price': [detail_item['neighborhood_median_price']],
            'compared_to_nearby_properties': [detail_item['compared_to_nearby_properties']]
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_property_price(self, property_selector):
        PRICE_SELECTOR = 'h2'
        price = get_element_selector(property_selector, PRICE_SELECTOR)
        return get_element_str(price, '::text')

    def _get_sold_municipality(self, element_selector):
        MUNICIPALITY_SELECTOR = 'span.gdvalh'
        municipality = get_element_selector(element_selector, MUNICIPALITY_SELECTOR)
        return get_element_str(municipality, '::text')

    def _get_property_info(self, property_selector):
        INFO_SELECTOR = 'ul.chQkbR'
        LI_BED_SELECTOR = 'li[data-testid="property-meta-beds"] > span[data-testid="meta-value"]'
        LI_BATH_SELECTOR = 'li[data-testid="property-meta-baths"] > span[data-testid="meta-value"]'
        LI_AREA_SELECTOR = 'li[data-testid="property-meta-sqft"] span.meta-value'

        info = get_element_selector(property_selector, INFO_SELECTOR)
        li_bed = get_element_selector(info, LI_BED_SELECTOR)
        li_bath = get_element_selector(info, LI_BATH_SELECTOR)
        li_area = get_element_selector(info, LI_AREA_SELECTOR)

        bedroom = get_element_str(li_bed, '::text').strip() if len(li_bed) else '-'
        bathroom = get_element_str(li_bath, '::text').strip() if len(li_bath) else '-'
        area = get_element_str(li_area, '::text').strip() if len(li_area) else '-'
        return bedroom, bathroom, area

    def _get_property_features(self, property_selector):
        FEATURE_SELECTOR = 'ul.ilWdQU'
        DIV_TYPE_SELECTOR = 'svg[data-testid="icon-home"] + div'
        DIV_YEAR_SELECTOR = 'svg[data-testid="icon-hammer"] + div'
        DATA_SELECTOR = 'div.eSplxE'

        feature = get_element_selector(property_selector, FEATURE_SELECTOR)
        div_type = get_element_selector(feature, DIV_TYPE_SELECTOR)
        div_year = get_element_selector(feature, DIV_YEAR_SELECTOR)
        data_type = get_element_selector(div_type, DATA_SELECTOR)
        data_year = get_element_selector(div_year, DATA_SELECTOR)

        property_type = get_element_str(data_type, '::text') if len(data_type) else '-'
        year = get_element_str(data_year, '::text') if len(data_year) else '-'
        return property_type, year

    def _get_compare_median(self, property_selector):
        COMPARE_PRICE_SELECTOR = property_selector.css('h2[data-testid="more-expensive-headline"]::text')
        MEAN_PRICE_SELECTOR = property_selector.css('h2[data-testid="neighborhood-median-price-card-headline"]::text')

        compare_price_value = COMPARE_PRICE_SELECTOR.get()
        mean_price_value = MEAN_PRICE_SELECTOR.get()

        return compare_price_value, mean_price_value


