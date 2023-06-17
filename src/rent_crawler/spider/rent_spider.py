import scrapy

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
                yield scrapy.Request(url=f"{url}/pg-{page_number}", callback=self.custom_parse)

    def custom_parse(self, response):
        self._response = response
        items = self._process()
        yield RentItem(list=items)

    def _process(self):
        SECTION_PARAM_SELECTOR = "section.PropertiesList_propertiesContainer__7NakV.PropertiesList_listViewGrid__TYNow"
        DIV_PARAM_SELECTOR = "div.BasePropertyCard_propertyCardWrap__zydWk"

        output = []
        sections = get_element_selector(self._response, SECTION_PARAM_SELECTOR)

        for section in sections:
            divs = get_element_selector(section, DIV_PARAM_SELECTOR)

            for div in divs:
                request_url = self._get_request_URL(div)
                municipality = self._get_rent_municipality(div)
                rental_type = self._get_rental_type(div)

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


