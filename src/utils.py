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

def get_request_URL(element_selector):
    request_url = ''
    DIV_PARAM_SELECTORS = [
        "div[data-testid='listing-card-wrapper-premiumplus'] > div",
        "div[data-testid='listing-card-wrapper-elite'] > div",
        "div[data-testid='listing-card-wrapper-elitepp'] > div",
        "div[data-testid='listing-card-wrapper-standard'] > div",
        "div[data-testid='listing-card-wrapper-standardpp'] > div"
    ]
    REQUEST_ATTR_SELECTOR = "div > a::attr(href)"

    for selector in DIV_PARAM_SELECTORS:
        divs_selector = get_element_selector(element_selector, selector)
        if len(divs_selector) >= 2:
            request_url = get_element_str(divs_selector[1], REQUEST_ATTR_SELECTOR)
            break

    return request_url

def spider_opened(spider):
    print(f"[{spider.name}_SPIDER_OPEN]: {spider.name}")

