import scrapy

from src import save_file, get_element_selector, get_request_URL, get_address_line1, get_address_line2, is_can_save_file
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
            "https://www.domain.com.au/sold-listings/"
        ]

        for url in urls:
            start_page = 1
            end_page = 51
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}?page={page_number}", callback=self.sold_parse)

    def sold_parse(self, response):
        self._response = response
        items = self._process()
        yield SoldItem(soldList = items)

    def _process(self):
        if is_can_save_file():
            save_file(
                spider=self,
                folder_name=self.folder_name,
                name=f'page_{self._response.url.split("=")[-1]}.html',
                content=self._response.body
            )

        UL_PARAM_SELECTOR = "ul[data-testid=\"results\"]"
        LI_PARAM_SELECTOR = "li[data-testid]"

        output = []
        uls_selector = get_element_selector(self._response, UL_PARAM_SELECTOR)

        for ul_selector in uls_selector:
            lis_selector = get_element_selector(ul_selector, LI_PARAM_SELECTOR)

            for li_selector in lis_selector:
                request_url = get_request_URL(li_selector)
                address_line_1 = get_address_line1(li_selector)
                address_line_2 = get_address_line2(li_selector)

                if len(request_url) > 0 and len(address_line_1) > 0 and len(address_line_2) > 0:
                    city, region, postcode = address_line_2
                    output.append({
                        'url': request_url,
                        'address': address_line_1,
                        'city': city,
                        'region': region,
                        'postcode': postcode,
                        'endPage': False
                    })
        output[len(output)-1]['endPage'] = True
        return output

