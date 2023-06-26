import scrapy
import os
import pandas as pd
import csv
import time

from src import save_file, get_element_selector, get_element_str, is_can_save_file
from src.rent_crawler import RentItem


class RentSpider(scrapy.Spider):
    name = "rent"
    folder_name = "rent"
    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'src.rent_crawler.RentMiddleware': 1
        },
        'ITEM_PIPELINES': {
            'src.rent_crawler.RentPipeline': 1
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None

    def start_requests(self):
        urls = [
            "https://www.realtor.com/apartments/New-York"
        ]

        for url in urls:
            start_page = 1
            end_page = 206
            for page_number in range(start_page, end_page):
                time.sleep(30)
                yield scrapy.Request(url=f"{url}/pg-{page_number}", callback=self.custom_parse)


    def custom_parse(self, response):
        self._response = response
        items = self._process()
        yield RentItem(list=items)

    def _process(self):
        #SECTION_PARAM_SELECTOR = "section.PropertiesList_propertiesContainer__7NakV.PropertiesList_listViewGrid__TYNow"
        SECTION_PARAM_SELECTOR = "section.PropertiesList_propertiesContainer__7NakV"
        DIV_PARAM_SELECTOR = "div.BasePropertyCard_propertyCardWrap__zydWk"

        output = []
        sections = get_element_selector(self._response, SECTION_PARAM_SELECTOR)

        for section in sections:
            divs = get_element_selector(section, DIV_PARAM_SELECTOR)

            for div in divs:
                from src.rent_crawler import RentDetailItem
                detail_item = RentDetailItem()

                DIV_PROPERTY_SELECTOR = 'div.Cardstyles__StyledCard-rui__sc-6oh8yg-0'
                property_selector = get_element_selector(div, DIV_PROPERTY_SELECTOR)
                print(property_selector)
                request_url = self._get_request_URL(div)
                municipality = self._get_rent_municipality(div)
                rental_type = self._get_rental_type(div)
                property_info = self._get_property_info(property_selector)
                price = self._get_property_price(property_selector)
                bedroom, bathroom, area = property_info
                print("municipality =", municipality, 'rental_type =', rental_type, 'price =', price, 'bedroom =',
                      bedroom, 'bathroom =', bathroom, 'area =', area)
                detail_item['price'] = price
                detail_item['municipality'] = municipality
                detail_item['rental_type'] = rental_type
                detail_item['bedroom'] = bedroom
                detail_item['bathroom'] = bathroom
                detail_item['area'] = area

                self._export_to_csv(detail_item)

                if len(request_url) and len(municipality) and len(rental_type):
                    output.append({
                        'url': request_url,
                        'municipality': municipality,
                        'rental_type': rental_type,
                        'endPage': False
                    })


        output[len(output) - 1]['endPage'] = True
        print(output)
        return output

    def _get_request_URL(self, element_selector):
        request_url = 'https://www.realtor.com'
        DIV_CONTAINER_SELECTOR = 'div.iclkph'
        REQUEST_ATTR_SELECTOR = "a::attr(href)"

        container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
        request_url += get_element_str(container, REQUEST_ATTR_SELECTOR)
        return request_url

    def _get_rent_municipality(self, element_selector):
        DIV_CONTAINER_SELECTOR = 'div.iclkph'
        DIV_ADDRESS_SELECTOR = 'div.card-address.truncate-line[data-testid="card-address"]'
        ADDRESS_SELECTOR = 'div.truncate-line[data-testid="card-address-2"]'
        container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
        div_address = get_element_selector(container, DIV_ADDRESS_SELECTOR)
        address = get_element_selector(div_address, ADDRESS_SELECTOR)
        if len(address):
            return get_element_str(address, '::text')
        else:
            return get_element_str(div_address, '::text')

    def _get_rental_type(self, element_selector):
        DIV_CONTAINER_SELECTOR = 'div.iclkph'
        RENTAL_TYPE_SELECTOR = 'div[data-testid="card-description"] > div'
        container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
        rental_type = get_element_selector(container, RENTAL_TYPE_SELECTOR)
        return get_element_str(rental_type, '::text')

    def _get_property_price(self, property_selector):
        PRICE_SELECTOR = 'div[data-testid="card-price"]'
        price = get_element_selector(property_selector, PRICE_SELECTOR)
        return get_element_str(price, '::text')

    def _get_property_info(self, property_selector):
        INFO_SELECTOR = 'ul.PropertyMetastyles__StyledPropertyMeta-rui__sc-1g5rdjn-0.ggAYob.card-meta'
        LI_BED_SELECTOR = 'li[data-testid="property-meta-beds"] > span[data-testid="meta-value"]::text'
        LI_BATH_SELECTOR = 'li[data-testid="property-meta-baths"] > span[data-testid="meta-value"]::text'
        LI_AREA_SELECTOR = 'li[data-testid="property-meta-sqft"] span.meta-value::text'

        info = get_element_selector(property_selector, INFO_SELECTOR)
        li_bed = get_element_str(info, LI_BED_SELECTOR)
        li_bath = get_element_str(info, LI_BATH_SELECTOR)
        li_area = get_element_str(info, LI_AREA_SELECTOR)

        bedroom = li_bed if li_bed else '-'
        bathroom = li_bath if li_bath else '-'
        area = li_area if li_area else '-'
        return bedroom, bathroom, area

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



