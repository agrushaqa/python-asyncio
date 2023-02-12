import asyncio
import datetime
import os.path
import time

from aiohttp import ClientSession

from api import get_list_api_urls_from_main_page, read_list_articles
from config import Config
from main_page import task_main_page, execute_list_tasks
from parse_main_page import parse_main_page_by_id


async def open_session(func, *args):
    async with ClientSession() as session:
        return await func(session, *args)


def refresh_page(get_subpages, get_list_links):
    while True:
        print("refresh main page")
        print(f"wait {Config.period_download} second...")
        print(datetime.datetime.now())
        time.sleep(Config.period_download)
        main_page = asyncio.run(open_session(task_main_page, path))
        updated_list_links = get_list_links(main_page)
        new_links = []
        for i_link in updated_list_links:
            if i_link not in list_links:
                new_links.append(i_link)
                list_links.append(i_link)
        if len(new_links) > 0:
            asyncio.run(open_session(get_subpages,
                                     new_links,
                                     Config.get_result_folder()))
        else:
            print("No new links..")


if __name__ == "__main__":
    path = os.path.join(
        Config.get_result_folder(),
        Config.saved_main_page
    )
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main_page_content = asyncio.run(open_session(task_main_page, path))
    if Config.use_api:
        list_links = get_list_api_urls_from_main_page(main_page_content)
        asyncio.run(open_session(read_list_articles,
                                 list_links,
                                 Config.get_result_folder()))
        refresh_page(read_list_articles, get_list_api_urls_from_main_page)
    else:
        list_links = parse_main_page_by_id(main_page_content)
        asyncio.run(open_session(execute_list_tasks,
                                 list_links,
                                 Config.get_result_folder()))
        refresh_page(execute_list_tasks, parse_main_page_by_id)
