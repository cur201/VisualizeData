from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"


    def start_requests(self):
        urls = [
            "https://www.domain.com.au/rent/melbourne-vic-3000/house/"
        ]
        setup = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': 'https://www.domain.com.au',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }

        for url in urls:
            start_page = 1
            end_page = 5
            for page_number in range(start_page, end_page):
                yield scrapy.Request(url=f"{url}?page={page_number}", headers=setup, callback=self.customParse)
    def customParse(self, response):

        #get the general page
        page = response.url.split("=")[-1]
        file_name = f"page_{page}.html"
        Path(file_name).write_bytes(response.body)
        self.log(f"finished write {file_name}")

        #get specific elements in each page
        resultList = response.css('ul[data-testid="results"] > li')
        for result in resultList:
            #get addr
            addr = response.css('span[data-testid="address-line1"]::text').get() + " " + response.css('span[data-testid="address-line2"]::text').get()
            #get rooms

            #get type

            #get price
            price = response.css('p[data-testid="listing-card-price"]::text').get()
            #get available status

            #get date sold




    # example
    def parse(self, response):
        for row in response.css("div.quote"):
            yield {
                "content": row.css("span.text::text").get(),
                "author": row.css("span > small.author::text").get()
            }