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
        # self._get_property_type(property_selector)

    def _get_rent_price(self, property_selector):
        rent_price = ''
        DIV_PRICE_SELECTOR = 'div[data-testid="listing-details__summary-title"]'
        div_selector = get_element_selector(property_selector, DIV_PRICE_SELECTOR)
        if div_selector:
            rent_price = get_element_str(div_selector[0], "::text")
        else:
            rent_price = '-'
        self.log(f"Rent price: {rent_price}")

    def _get_address(self, property_selector):
        address = ''
        # DIV_ADDRESS_SELECTOR = 'div[data-testid="listing-details__button-copy-wrapper"] > div > div'
        # TEXT_ADDRESS = 'div[data-testid="listing-details__button-copy-wrapper"] h1::text'
        # div_selector = get_element_selector(property_selector, DIV_ADDRESS_SELECTOR)
        # if len(div_selector) >= 2:
        #     address = get_element_str(div_selector, TEXT_ADDRESS)
        # else:
        #     address = "-"
        address = ''
        DIV_ADDRESS_SELECTOR = 'div[data-testid="listing-details__button-copy-wrapper"] > div > div > h1::text'
        div_selector = get_element_selector(property_selector, DIV_ADDRESS_SELECTOR)
        if div_selector:
            address = get_element_str(div_selector[0], '')
        else:
            address = '-'
        self.log(f"Address: {address}")

    def _get_property_info(self, property_selector):
        room_info = ''
        room_features_str = []
        DIV_PROPERTY_INFO_SELECTOR = "div[data-testid=\"property-features-wrapper\"] > div"
        SPAN_PROPERTY_SELECTOR = "span[data-testid=\"property-features-feature\"] > span"

        divs_selector = get_element_selector(property_selector, DIV_PROPERTY_INFO_SELECTOR)
        if len(divs_selector) >= 2:
            room_features = get_element_selector(divs_selector[1], SPAN_PROPERTY_SELECTOR)
            for feature in room_features:
                room_features_str.append(get_element_str(feature, "::text"))
        else:
            room_info = '-'
        room_info = ', '.join(room_features_str)
        self.log(f"Room Info: {room_info}")

    # def _get_property_type(self):
    #    pass