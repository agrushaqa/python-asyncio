import asyncio
import os.path

from aiohttp import ClientSession

from api import get_list_api_urls_from_main_page, read_list_articles
from config import Config
from main_page import task_main_page


async def open_session(func, *args):
    async with ClientSession() as session:
        return await func(session, *args)


if __name__ == "__main__":
    path = os.path.join(
        Config.get_result_folder(),
        Config.saved_main_page
    )
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main_page = asyncio.run(open_session(task_main_page, path))
    list_links = get_list_api_urls_from_main_page(main_page)
    asyncio.run(open_session(read_list_articles,
                             list_links,
                             Config.get_result_folder()))
