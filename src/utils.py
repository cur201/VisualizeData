from pathlib import Path
from src import RES_DIR


def get_element_selector(parent_selector, tag_selector):
    return parent_selector.css(tag_selector)


def get_element_str(parent_selector, tag_selector):
    return parent_selector.css(tag_selector).get()


def save_file(spider, folder_name, name, content):
    file_name = f"{name}"
    file_name = '/'.join([RES_DIR, folder_name, file_name])
    Path(file_name).write_bytes(content)
    if spider is not None:
        print(f"[{spider.name}_UTILS_SAVE_FILE]: {file_name}")
    else:
        print(f"[UTILS_SAVE_FILE]: {file_name}")


def get_request_URL(element_selector, spider):
    request_url = 'https://www.realtor.com'
    if spider == 'rent':
        DIV_CONTAINER_SELECTOR = 'div.iclkph'
    else:
        DIV_CONTAINER_SELECTOR = 'div.card-box.type-srp-result'
    REQUEST_ATTR_SELECTOR = "a::attr(href)"

    container = get_element_selector(element_selector, DIV_CONTAINER_SELECTOR)
    request_url += get_element_str(container, REQUEST_ATTR_SELECTOR)
    return request_url


def spider_opened(spider):
    print(f"[{spider.name}_SPIDER_OPEN]: {spider.name}")

def get_property_price(property_selector, spider):
    if spider == 'rent':
        PRICE_SELECTOR = 'div.Price__Component-rui__x3geed-0.hAEpgA.heading'
    else:
        PRICE_SELECTOR = 'h2.ignleU'
    price = get_element_selector(property_selector, PRICE_SELECTOR)
    return get_element_str(price, '::text')


def is_can_save_file():
    # todo: add condition for saving file
    return True
