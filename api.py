import asyncio
import os

from aiohttp import ClientSession

from api_json import (get_json_from_text, get_kids_pages, get_url_from_param,
                      get_url_from_text_param)
from config import Config
from links import Links, get_last_part
from main_page import get_sub_page, save_page_as_binary, save_page_as_text
from parse_main_page import _get_parent_tag, remove_non_latin_letters
from url_ext import UrlExt, get_extension


async def read_list_articles(
        session: ClientSession,
        urls: list,
        result_folder: str):
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(
            get_sub_page(session, Links(path=url.path,
                                        name=url.name,
                                        parent_url=Config.site_base_url
                                        ), {})))
    for task in tasks:
        page = await task
        print(page.path)
        json_text = get_json_from_text(page.content)
        external_links = get_url_from_text_param(json_text)
        kids_pages = get_kids_pages(json_text)
        if kids_pages is not None:
            for kid_page in kids_pages:
                tasks.append(asyncio.create_task(
                    get_sub_page(session,
                                 Links(path=f"{Config.api_base_url}"
                                            f"{kid_page}"
                                            f"{Config.api_params_url}",
                                       name=str(kid_page),
                                       parent_url=page.path
                                       ), {})))

        if len(json_text) > 0:
            url_from_tag = get_url_from_param(json_text)
            if url_from_tag is not None:
                external_links.append(url_from_tag)
        filename = os.path.join(result_folder,
                                str(page.name) + get_extension(page.ext))
        task2 = asyncio.create_task(save_page_as_text(filename, page.content))
        await task2
        if len(external_links) > 0:
            sub_folder = os.path.join(result_folder, page.name)
            if not os.path.exists(sub_folder):
                os.makedirs(sub_folder)
            await get_external_pages(session,
                                     page.path,
                                     external_links,
                                     sub_folder)


async def get_external_pages(session: ClientSession,
                             parent_url: str,
                             urls: list,
                             result_folder: str):
    external_tasks = []
    print("get_external_pages")
    for url in urls:
        print("for url:")
        print(url.path)
        print("name:")
        print(remove_non_latin_letters(get_last_part(url.path)))
        page_name = remove_non_latin_letters(get_last_part(url.path))
        if page_name[-5:] == ".html":
            # todo сделать поддержку всех расширений
            page_name = page_name[:-5]
        external_tasks.append(asyncio.create_task(
            get_sub_page(session, Links(path=url.path,
                                        name=page_name,
                                        parent_url=parent_url), {})))
    for external_task in external_tasks:
        page = await external_task
        filename = os.path.join(result_folder,
                                page.name + get_extension(page.ext))
        if page.ext == UrlExt.PDF:
            external_task2 = asyncio.create_task(
                save_page_as_binary(filename, page.content))
        else:
            external_task2 = asyncio.create_task(
                save_page_as_text(filename, page.content))
        await external_task2


def get_list_api_urls_from_main_page(html_doc):
    parent_tag = _get_parent_tag(html_doc)
    result = []
    for link in parent_tag:
        result.append(
            Links(
                path=f"{Config.api_base_url}{link['id']}"
                     f"{Config.api_params_url}",
                name=link['id'],
                parent_url=Config.site_base_url
            ))
    return result
