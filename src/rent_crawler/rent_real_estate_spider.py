from pathlib import Path

import scrapy

from src.config import RES_DIR

class RealEstateSpider(scrapy.Spider):
    name = "rent_real_estate"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = None

    def start_requests(self):
        urls = [
            "https://www.domain.com.au/rent/"
        ]

        for url in urls:
            start_page = 1
            end_page = 4
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}?page={page_number}", callback=self.customParse)

        self._response = None

    def _is_can_save_file(self):
        # todo: add condition for saving file
        return True
    def _save_file(self, url, content):
        page = url.split("=")[-1]
        file_name = '/'.join([RES_DIR, f"rent", f"page_{page}.html"])
        Path(file_name).write_bytes(content)
        self.log(f"finished write {file_name}")

    def _get_element_selector(self, parent_selector, tag_selector):
        return parent_selector.css(tag_selector)

    def _get_element_str(self, parent_selector, tag_selector):
        return parent_selector.css(tag_selector).get()

    def _process(self):

        if self._is_can_save_file() == True:
            self._save_file(self._response.url, self._response.body)

        uls_selector = self._get_element_selector(self._response, "ul[data-testid=\"results\"]")
        for ul_selector in uls_selector:
            lis_selector = self._get_element_selector(ul_selector, "li[data-testid]")
            for li_selector in lis_selector:
                rent_price = 0
                divs_selector = self._get_element_selector(li_selector, "div[data-testid=\"listing-card-wrapper-premiumplus\"] > div")
                if len(divs_selector) < 2:
                    divs_selector = self._get_element_selector(li_selector, "div[data-testid=\"listing-card-wrapper-elite\"] > div")

                if len(divs_selector) >= 2:
                    price_selector = self._get_element_selector(divs_selector[1], "p[data-testid=\"listing-card-price\"]")
                    if len(price_selector) >= 1:
                        rent_price = self._get_element_str(divs_selector[1], "p[data-testid=\"listing-card-price\"]::text")

                self.log(f"Rent price: {rent_price}")

    def customParse(self, response):
        self._response = response
        self._process()



