# Задание
Ycrawler
## Задание: 
написать асинхронный краулер для новостного сайта news.ycombinator.com:
краулер начинает обкачивать сайт с корня news.ycombinator.com/
краулер должен обкачивать топ новостей, т.е. первые 30 на корневой станице,
после чего ждать появления новых новостей в топе, которых он раньше не видел
для того, чтобы "скачать" новость нужно скачать непосредственно страницу 
на которую она ведет и загрузить все страницы по ссылкам в комментариях к новости
внутри скачанных страниц далее новые ссылки искать не нужно
скачанная новость со всеми скачанными страницами из комментариев должна лежать в отдельной папке на диске
разрешается использовать стандартную библиотеку, aiohttp, aiofiles,beautifulsoup.
цикл обкачки должен запускаться каждые N секунд
Python 3.7+
# Цель задания:
 поближе познакомиться с асинхронным программированием, получить опыт написания и отладки асинхронных программ.
# Критерии успеха: 
задание обязательно, 
критерием успеха является работающий согласно заданию код, для которого проверено соответствие pep8, написана
документация с примерами запуска, в README, например. Далее успешность определяется code review.

# Особенности реализации
Смотри файл url_ext.py сейчас из бинарных форматов поддерживается только pdf
"application/pdf" in headers["Content-Type"]:
Остальные считаются текстовыми. 
Если среди файлов будет файл с расширением txt, то возможно тип этого файла не распознался.
# requirements.txt
## create
pip freeze > requirements.txt
## use
pip install -r requirements.txt

# code style
## isort
python -m pip install isort
### run 
isort .
## mypy
python -m pip install mypy
### run 
mypy .
## flake8
python -m pip install flake8
### run
flake8 --exclude venv,docs --ignore=F401
## code coverage
pip install coverage
### run
coverage run C:\Users\agrusha\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\behave\__main__.py
в файле .coveragerc нужно указать исходники

# Pytest - Run Tests in Parallel
## install
```pip install pytest-xdist```

also:
https://pypi.org/project/pytest-parallel/
## run
```pytest -n 2 test_common.py```


# Замечания
при асинхронной загрузке я получаю ошибку
 Sorry, we're not able to serve your requests this quickly. 

## Cкачивание страницы curl
curl.exe --insecure https://news.ycombinator.com/item?id=34722118