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
            yield scrapy.Request(url=url, callback=self.sold_detail_parse,
                                 cb_kwargs=dict(sold_date=sold_date))

    def sold_detail_parse(self, response, sold_date):
        self._response = response
        self._detail_process(sold_date)

    def _detail_process(self, sold_date):
        from src.sold_crawler import SoldDetailItem
        detail_item = SoldDetailItem()
        DIV_PROPERTY_SELECTOR = 'div.hiyzem'
        DIV_DETAIL_SELECTOR = 'div.etUKSQ'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)[0]
        # detail_selector = get_element_selector(self._response, DIV_DETAIL_SELECTOR)[0]
        # print(property_selector)
        # print(detail_selector)

        price = self._get_property_price(property_selector)
        municipality = self._get_sold_municipality(property_selector)
        bedroom, bathroom, area = self._get_property_info(property_selector)
        type, year = self._get_property_features(property_selector)
        # compare, median = self._get_compare_median(self._response)
        detail_item['price'] = price
        detail_item['municipality'] = municipality
        detail_item['sold_date'] = sold_date
        detail_item['property_type'] = type
        detail_item['bedroom'] = bedroom
        detail_item['bathroom'] = bathroom
        detail_item['area'] = area
        detail_item['year_built'] = year
        # self._export_to_csv(detail_item)

    def _export_to_csv(self, detail_item):
        export_file = 'sold-data.csv'
        output_dir = './res/data/'
        output_path = os.path.join(output_dir, export_file)

        if not os.path.exists(output_path):
            with open(output_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['price', 'municipality', 'sold_date ', 'property_type', 'bedroom', 'bathroom', 'area',
                                 'year_built'])

        data = {
            'price': [detail_item['price']],
            'municipality': [detail_item['municipality']],
            'sold_date': [detail_item['sold_date']],
            'property_type': [detail_item['property_type']],
            'bedroom': [detail_item['bedroom']],
            'bathroom': [detail_item['bathroom']],
            'area': [detail_item['area']],
            'year_built': [detail_item['year_built']],
        }
        df = pd.DataFrame(data)
        df.to_csv(output_path, mode='a', header=False, index=False)

    def _get_property_price(self, property_selector):
        PRICE_SELECTOR = 'h2.ignleU'
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
        LI_AREA_SELECTOR = 'li[data-testid="property-meta-sqft"]'

        info = get_element_selector(property_selector, INFO_SELECTOR)
        li_bed = get_element_selector(info, LI_BED_SELECTOR)
        li_bath = get_element_selector(info, LI_BATH_SELECTOR)
        li_area = get_element_selector(info, LI_AREA_SELECTOR)

        bedroom = get_element_str(li_bed, '::text') if len(li_bed) else '-'
        bathroom = get_element_str(li_bath, '::text') if len(li_bath) else '-'
        area = get_element_str(li_area, '::text') if len(li_area) else '-'
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

        type = get_element_str(data_type, '::text') if len(data_type) else '-'
        year = get_element_str(data_year, '::text') if len(data_year) else '-'
        return type, year


    def _get_compare_median(self, property_selector):
        COMPARE_PRICE_SELECTOR = 'h2[data-testid="more-expensive-headline"]'
        MEAN_PRICE_SELECTOR = 'h2[data-testid="neighborhood-median-price-card-headline"]'
        test = 'div.joCQGe'
        div = get_element_selector(property_selector, DIV_SELECTOR)[0]
        print(div)
        print(get_element_str(div, '::text'))
        # compare_price = get_element_selector(div, COMPARE_PRICE_SELECTOR)
        # mean_price = get_element_selector(div, MEAN_PRICE_SELECTOR)
        # print(get_element_selector(div, test))
        # print(compare_price, mean_price)
        # print(get_element_str(compare_price, '::text'), get_element_str(mean_price, '::text'))
        return 1, 2


