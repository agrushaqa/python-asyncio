from dataclasses import dataclass


@dataclass
class Links:
    path: str
    name: str
    content: str = ""
    ext: int = 0
    parent_url: str = ""
    # is_url: bool


def get_last_part(url: str):
    last_symbol = url[len(url) - 1]
    if last_symbol == "/":
        my_url = url[: -1]
        return my_url[my_url.rindex("/") + 1:]
    return url[url.rindex("/") + 1:]
