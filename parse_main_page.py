import regex
from bs4 import BeautifulSoup
from links import Links


def _get_parent_tag(html_doc, id_table='hnmain',
                    parent_tag_name="tr",
                    parent_tag_class="athing"):
    soup = BeautifulSoup(html_doc, 'html.parser')
    table = soup.find(id=id_table)
    parent_tag = table.find_all(parent_tag_name, class_=parent_tag_class)
    return parent_tag


def parse_main_page_by_id(html_doc, url):
    parent_tag = _get_parent_tag(html_doc)
    result = []
    for link in parent_tag:
        result.append(Links(path=f"{url}{link['id']}",
                            name=remove_non_latin_letters(
                                link.find('span', class_='titleline'
                                          ).find('a').contents[0])
                            ))
    return result


def remove_non_latin_letters(string, max_length=40):
    return regex.sub(r'[^\p{Latin} ]', u'', string)[:max_length]


def is_url(text_for_check) -> bool:
    pattern = regex.compile(
        r'^(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,5}(\/\S*)*$')
    if regex.fullmatch(pattern, text_for_check):
        return True
    else:
        return False
