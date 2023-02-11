import os.path
import pathlib


class Config:
    api_base_url = "https://hacker-news.firebaseio.com/v0/item/"
    api_params_url = ".json?print=pretty"
    saved_main_page = "mainpage.html"
    saved_file_encoding = "utf-8"
    site_base_url = "https://news.ycombinator.com/"
    sub_pages_base_url = "https://news.ycombinator.com/item?id="
    url_regexp = r'https\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,5}\/' \
                 r'[a-zA-Z&=.?/0-9]*'

    @staticmethod
    def get_result_folder():
        return os.path.join(
            pathlib.Path(__file__).parent.resolve(),
            "result"
        )

    @staticmethod
    def get_filename_list_results():
        return os.path.join(
            pathlib.Path(__file__).parent.resolve(),
            "result",
            "result.yml"
        )
