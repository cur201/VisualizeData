﻿import scrapy

from src import save_file, get_element_selector, get_element_str
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
            "https://www.domain.com.au/rent/"
        ]

        for url in urls:
            start_page = 1
            end_page = 3
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}?page={page_number}", callback=self.custom_parse)

    def _is_can_save_file(self):
        # todo: add condition for saving file
        return True

    def _get_request_URL(self, li_selector):
        request_url = ''
        DIV_PARAM_SELECTOR = "div[data-testid=\"listing-card-wrapper-premiumplus\"] > div"
        ALTER_DIV_PARAM_SELECTOR = "div[data-testid=\"listing-card-wrapper-elite\"] > div"
        REQUEST_ATTR_SELECTOR = "div > a::attr(href)"

        divs_selector = get_element_selector(li_selector, DIV_PARAM_SELECTOR)

        if len(divs_selector) < 2:
            divs_selector = get_element_selector(li_selector, ALTER_DIV_PARAM_SELECTOR)

        if len(divs_selector) >= 2:
            request_url = get_element_str(divs_selector[1], REQUEST_ATTR_SELECTOR)

        return request_url

    def _process(self):
        if self._is_can_save_file() == True:
            save_file(
                spider=self,
                folder_name=self.folder_name,
                name=f'page_{self._response.url.split("=")[-1]}.html',
                content=self._response.body
            )

        # print(f"{self._response.meta}")
        UL_PARAM_SELECTOR = "ul[data-testid=\"results\"]"
        LI_PARAM_SELECTOR = "li[data-testid]"

        output = []
        uls_selector = get_element_selector(self._response, UL_PARAM_SELECTOR)

        for ul_selector in uls_selector:
            lis_selector = get_element_selector(ul_selector, LI_PARAM_SELECTOR)

            for li_selector in lis_selector:
                request_url = self._get_request_URL(li_selector)
                if len(request_url) > 0:
                    output.append({
                        'url': request_url,
                        'endPage': False
                    })
        output[len(output)-1]['endPage'] = True
        return output

    def custom_parse(self, response):
        self._response = response
        items = self._process()
        yield RentItem(list = items)