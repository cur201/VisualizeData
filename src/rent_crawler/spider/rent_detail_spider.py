import scrapy
from src import get_element_selector, get_element_str

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
        self._get_rent_price(property_selector)
        self._get_address(property_selector)
        self._get_property_info(property_selector)
        self._get_property_type(property_selector)

    def _get_rent_price(self, property_selector):
        rent_price = ''
        DIV_PRICE_SELECTOR = 'div[data-testid="listing-details__summary-title"]'
        div_selector = get_element_selector(property_selector, DIV_PRICE_SELECTOR)
        if len(div_selector) >= 1:
            rent_price = get_element_str(div_selector[0], "::text")
        else:
            rent_price = '-'
        print(f"Rent price: {rent_price}")

    def _get_address(self, property_selector):
        address = ''
        DIV_ADDRESS_SELECTOR = 'div[data-testid="listing-details__button-copy-wrapper"]'
        TEXT_ADDRESS = 'h1::text'
        div_selector = get_element_selector(property_selector, DIV_ADDRESS_SELECTOR)
        if len(div_selector) >= 1:
            address = get_element_str(div_selector, TEXT_ADDRESS)
        else:
            address = '-'
        print(f"Address: {address}")

    def _get_property_info(self, property_selector):
        property_info = ''
        property_numbers_str = []
        property_type_str = []

        DIV_PROPERTY_INFO_SUMMARY = 'div[data-testid="property-features"]'
        DIV_PROPERTY_INFO_SELECTOR = 'span[data-testid="property-features-feature"] > span'
        SPAN_PROPERTY_INFO_TYPE_SELECTOR = 'span[data-testid="property-features-text"]'
        property_div_selector = get_element_selector(property_selector, DIV_PROPERTY_INFO_SUMMARY)

        property_div_selector = get_element_selector(property_div_selector, DIV_PROPERTY_INFO_SELECTOR)
        for selector in property_div_selector:
            property_numbers_str.append(get_element_str(selector, '::text'))
            property_type = get_element_selector(selector, SPAN_PROPERTY_INFO_TYPE_SELECTOR)
            property_type_str.append(get_element_str(property_type, '::text'))

        if len(property_numbers_str) >= 1:
            property_info = ', '.join([f"{number} {ptype}" for number, ptype in zip(property_numbers_str, property_type_str)])
        else:
            property_info = '-'
        print(f"Property Info: {property_info}")


    def _get_property_type(self, property_selector):

        property_type = ''

        DIV_PROPERTY_TYPE = 'div[data-testid="listing-summary-property-type"] > span'
        property_type_selector = get_element_selector(property_selector, DIV_PROPERTY_TYPE)

        if len(property_type_selector) >=1 :
            property_type = get_element_str(property_type_selector[0], "::text")
        else:
            property_type = ''
        print(f"Property Type: {property_type}")