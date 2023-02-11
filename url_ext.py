from enum import Enum


class UrlExt(Enum):
    UNKNOWN = 0
    PDF = 1
    JSON = 2
    HTML = 3


def get_url_ext(headers):
    if "application/pdf" in headers["Content-Type"]:
        return UrlExt.PDF
    if "application/json" in headers["Content-Type"]:
        return UrlExt.JSON
    if "text/html" in headers["Content-Type"]:
        return UrlExt.HTML
    return UrlExt.UNKNOWN


def get_extension(ext_type):
    if ext_type == UrlExt.PDF:
        return ".pdf"
    if ext_type == UrlExt.JSON:
        return ".json"
    if ext_type == UrlExt.HTML:
        return ".html"
    return ".txt"
