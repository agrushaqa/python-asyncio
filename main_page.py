import os.path
import random
import time

from aiohttp import ClientSession
from threading import Thread
import asyncio
from links import Links


async def get_page(url: Links, params) -> Links:
    print(f"send:{url.path}")
    async with ClientSession() as session:
        async with session.get(url=url.path, params=params) as response:
            url.content = await response.text()
            return url


async def task_main_page(filename: str) -> str:
    main_page = Links(path="https://news.ycombinator.com/",
                      name='main page')
    task1 = asyncio.create_task(get_page(main_page, {}))
    main_page = await task1
    task2 = asyncio.create_task(save_main_page(filename, main_page.content))
    await task2
    return main_page.content


async def execute_list_tasks(result_folder: str, subpages: list):
    tasks = []
    for page in subpages:
        tasks.append(asyncio.create_task(
            get_page(Links(path=page.path,
                           name=page.name), {})))
    for task in tasks:
        page = await task
        filename = os.path.join(result_folder, page.name + ".html")
        task2 = asyncio.create_task(save_main_page(filename, page.content))
        await task2
        time.sleep(60)  # TODO удалить - это для обхода ошибки - > 30sec
        #  Sorry, we're not able to serve your requests this quickly.
        # await asyncio.sleep(random.randrange(5, 240))
        # workaround for error:
        # Sorry, we're not able to serve your requests this quickly.


async def save_main_page(filename: str, data: str):
    with open(filename, 'w+', encoding="utf-8") as file:
        tr = Thread(target=file.write, args=(data,))
        tr.start()
