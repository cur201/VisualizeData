import scrapy
import time
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
        print("Pass init")


    def start_requests(self):
        urls = [
            "https://www.realtor.com/realestateandhomes-search/New-York/show-recently-sold"
        ]

        for url in urls:
            start_page = 1
            end_page = 206
            time.sleep(30)
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}/pg-{page_number}", callback=self.sold_parse)
                print("Pass request")

    def sold_parse(self, response):
        self._response = response
        print("Pass get response")
        items = self._process()
        print("Pass process")
        yield SoldItem(soldList=items)

    def _process(self):
        SECTION_PARAM_SELECTOR = 'ul[data-testid="property-list-container"]'
        DIV_PARAM_SELECTOR = 'li[data-testid="result-card"]'

        output = []

        sections = self._response.css(SECTION_PARAM_SELECTOR)
        print(sections)
        for section in sections:
            divs = section.css(DIV_PARAM_SELECTOR)
            print(divs)
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
        if len(output) > 0:
            output[len(output) - 1]['endPage'] = True
        return output

    def _get_request_URL(self, element_selector):
        request_url = 'https://www.realtor.com'
        ANCHOR_SELECTOR = 'a[data-testid="property-anchor"]::attr(href)'

        href = element_selector.css(ANCHOR_SELECTOR).get()
        if href:
            request_url += href
        return request_url

    def _get_sold_date(self, element_selector):
        SOLD_DATE_CONTAINER_SELECTOR = 'div[data-testid="sold"]'
        SOLD_DATE_TEXT_SELECTOR = 'span.statusText'

        container = get_element_selector(element_selector, SOLD_DATE_CONTAINER_SELECTOR)
        sold_date = get_element_str(container, SOLD_DATE_TEXT_SELECTOR)
        return sold_date
