import asyncio
import os.path
import time
from threading import Thread

import yaml
from aiohttp import ClientSession

from api_json import get_md5
from config import Config
from links import Links
from url_ext import UrlExt, get_url_ext


async def get_page(session: ClientSession, url: Links, params) -> Links:
    print(f"send:{url.path}")
    async with session.get(url=url.path, params=params) as response:
        url.content = await response.text()
        return url


async def get_sub_page(session, url: Links, params) -> Links:
    print(f"(sub_page) send:{url.path}")
    try:
        async with session.get(url=url.path, params=params) as response:
            await set_page_info(url, response.headers)
            url.ext = get_url_ext(response.headers)
            if "application/pdf" in response.headers["Content-Type"]:
                url.content = await response.read()
            else:
                url.content = await response.text()
            print()
            return url
    except Exception as ex:
        # TODO сейчас повторая попытка в случае ошибки не осуществляется
        await set_page_info(url, {"exception": str(ex)})
        url.ext = UrlExt.UNKNOWN
        return url


async def set_page_info(url: Links, headers):
    data = dict(parent_url=url.parent_url,
                url=url.path,
                name=url.name,
                md5=get_md5(url.path),
                header=str(headers.items()))
    with open(Config.get_filename_list_results(), 'a') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
        outfile.write('\n')


async def task_main_page(session, filename: str) -> str:
    main_page = Links(path=Config.site_base_url,
                      name='main page')
    task1 = asyncio.create_task(get_page(session, main_page, {}))
    main_page = await task1
    task2 = asyncio.create_task(save_page_as_text(filename, main_page.content))
    await task2
    return main_page.content


async def execute_list_tasks(session, result_folder: str, subpages: list):
    tasks = []
    for page in subpages:
        tasks.append(asyncio.create_task(
            get_sub_page(session, Links(path=page.path,
                                        name=page.name), {})))
    for task in tasks:
        page = await task
        filename = os.path.join(result_folder, page.name + ".html")
        task2 = asyncio.create_task(save_page_as_text(filename, page.content))
        await task2
        time.sleep(30)  # TODO удалить - это для обхода ошибки - > 30sec
        #  Sorry, we're not able to serve your requests this quickly.
        # await asyncio.sleep(random.randrange(5, 240))
        # workaround for error:
        # Sorry, we're not able to serve your requests this quickly.


async def save_page_as_text(filename: str, data: str):
    with open(filename, 'w+', encoding=Config.saved_file_encoding) as file:
        tr = Thread(target=file.write, args=(data,))
        tr.start()


async def save_page_as_binary(filename: str, data: str):
    with open(filename, "wb") as file:
        tr = Thread(target=file.write, args=(data,))
        tr.start()
