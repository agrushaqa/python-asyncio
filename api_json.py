import hashlib
import html
import json
import re

from config import Config
from links import Links, get_last_part
from parse_main_page import remove_non_latin_letters


def get_json_from_text(text):
    return json.loads(text)


def get_url_from_param(json_text: json):
    # return None if absent
    url = json_text.get("url")
    if url is not None:
        return Links(path=url,
                     name=remove_non_latin_letters(get_last_part(url)))
    return None


def get_kids_pages(json_text: json):
    return json_text.get("kids")


def get_url_from_text_param(json_text: json):
    text = json_text.get("text")
    result = []
    if text:
        decoded_text = html.unescape(text)
        list_urls = find_all_urls_in_text(decoded_text)
        for i_url in list_urls:
            result.append(Links(path=i_url,
                                name=remove_non_latin_letters(
                                    get_last_part(i_url))))
    return []


def get_md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def find_all_urls_in_text(json_text):
    return re.findall(Config.url_regexp, json_text)
