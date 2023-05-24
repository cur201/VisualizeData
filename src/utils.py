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

def get_address(property_selector):
    address = ''
    DIV_ADDRESS_SELECTOR = 'div[data-testid="listing-details__button-copy-wrapper"]'
    TEXT_ADDRESS = 'h1::text'
    div_selector = get_element_selector(property_selector, DIV_ADDRESS_SELECTOR)
    if len(div_selector) >= 1:
        address = get_element_str(div_selector, TEXT_ADDRESS)
    else:
        address = '-'
    print(f"Address: {address}")
    return address

def get_property_info(property_selector):
    property_info = ''
    property_numbers_str = []
    property_type_str = []

    DIV_PROPERTY_INFO_SUMMARY = 'div[data-testid="property-features"]'
    DIV_PROPERTY_INFO_SELECTOR = 'span[data-testid="property-features-feature"] > span'
    SPAN_PROPERTY_INFO_TYPE_SELECTOR = 'span[data-testid="property-features-text"]'
    property_div_selector = get_element_selector(property_selector, DIV_PROPERTY_INFO_SUMMARY)

    property_div_selector = get_element_selector(property_div_selector, DIV_PROPERTY_INFO_SELECTOR)
    for selector in property_div_selector:
        property_numbers_str.append(get_element_str(selector, '::text'))
        property_type = get_element_selector(selector, SPAN_PROPERTY_INFO_TYPE_SELECTOR)
        property_type_str.append(get_element_str(property_type, '::text'))

    if len(property_numbers_str) >= 1:
        property_info = ', '.join([f"{number} {ptype}" for number, ptype in zip(property_numbers_str, property_type_str)])
    else:
        property_info = '-'
    print(f"Property Info: {property_info}")
    return property_info


def get_property_type(property_selector):

    property_type = ''

    DIV_PROPERTY_TYPE = 'div[data-testid="listing-summary-property-type"] > span'
    property_type_selector = get_element_selector(property_selector, DIV_PROPERTY_TYPE)

    if len(property_type_selector) >=1 :
        property_type = get_element_str(property_type_selector[0], "::text")
    else:
        property_type = ''
    print(f"Property Type: {property_type}")
    return property_type

def get_date_sold(property_selector):
    date_sold = ''

    DIV_DATE_SOLD = 'span[data-testid="listing-details__listing-tag"]'
    date_sold_selector = get_element_selector(property_selector, DIV_DATE_SOLD)
    if len(date_sold_selector) >=1 :
        date_sold = get_element_str(date_sold_selector[0], "::text")
    else:
        date_sold = ''
    print(f'Date Sold: {date_sold}')
    return date_sold