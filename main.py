import asyncio
import os.path
import pathlib
from main_page import task_main_page, execute_list_tasks
from parse_main_page import parse_main_page_by_id

if __name__ == "__main__":
    result_folder = os.path.join(
        pathlib.Path(__file__).parent.resolve(),
        "result"
    )
    path = os.path.join(
        result_folder,
        "mainpage.html"
    )
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    main_page = asyncio.run(task_main_page(path))
    list_links = parse_main_page_by_id(main_page,
                                       "https://news.ycombinator.com/item?id=")
    print(list_links)
    asyncio.run(execute_list_tasks(result_folder, list_links))
