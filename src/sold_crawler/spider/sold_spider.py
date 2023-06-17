import scrapy

from src import save_file, get_element_selector, get_element_str, is_can_save_file
from src.sold_crawler import SoldItem


class SoldSpider(scrapy.Spider):
    name = 'sold'
    folder_name = 'sold'
    custom_settings = {
        'SPIDER_MIDDLEWARES': {
            'src.sold_crawler.SoldMiddleware': 1
        },
        'ITEM_PIPELINES': {
            'src.sold_crawler.SoldPipeline': 1
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None

    def start_requests(self):
        urls = [
            "https://www.realtor.com/realestateandhomes-search/New-York/show-recently-sold"
        ]

        for url in urls:
            start_page = 1
            end_page = 2
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}/pg-{page_number}", callback=self.sold_parse)

    def sold_parse(self, response):
        self._response = response
        items = self._process()
        yield SoldItem(soldList=items)

    def _process(self):
        SECTION_PARAM_SELECTOR = 'section.PropertiesList_propertiesContainer__j6ct_.PropertiesList_listViewGrid__oGuSL'
        DIV_PARAM_SELECTOR = 'div.BasePropertyCard_propertyCardWrap__J0xUj'

        output = []
        sections = get_element_selector(self._response, SECTION_PARAM_SELECTOR)
        print(sections)
        print(sections)

        for section in sections:
            divs = get_element_selector(section, DIV_PARAM_SELECTOR)
            for div in divs:
                request_url = self._get_request_URL(div)
                sold_date = self._get_sold_date(div)

                print(request_url, sold_date)

                if len(request_url) and len(sold_date):
                    output.append({
                        'url': request_url,
                        'sold_date': sold_date,
                        'endPage': False
                    })
        output[len(output) - 1]['endPage'] = True
        return output

    def _get_request_URL(self, element_selector):
        request_url = 'https://www.realtor.com'
        DIV_CONTAINER_SELECTOR = 'div[data-testid="card-content"]'
        REQUEST_ATTR_SELECTOR = "a::attr(href)"

        container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
        request_url += get_element_str(container, REQUEST_ATTR_SELECTOR)
        return request_url

    def _get_sold_date(self, element_selector):
        DIV_CONTAINER_SELECTOR = 'div[data-testid="card-content"]'
        SOLD_DATE_SELECTOR = 'div.message'
        container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
        sold_date = get_element_selector(container, SOLD_DATE_SELECTOR)
        return get_element_str(sold_date, "::text")
