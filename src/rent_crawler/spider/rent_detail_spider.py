import scrapy
from src import get_element_selector, get_element_str, get_address, get_property_info, get_property_type


class RentDetailSpider(scrapy.Spider):
    name = "rent_detail"
    folder_name = "rent_detail"

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
        DIV_PROPERTY_SELECTOR = 'div[data-testid="listing-details__summary-left-column"]'
        property_selector = get_element_selector(self._response, DIV_PROPERTY_SELECTOR)
        rent_price = self._get_rent_price(property_selector)
        address = get_address(property_selector)
        property_info = get_property_info(property_selector)
        property_type = get_property_type(property_selector)

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

