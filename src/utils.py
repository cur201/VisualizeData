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


def spider_opened(spider):
    print(f"[{spider.name}_SPIDER_OPEN]: {spider.name}")