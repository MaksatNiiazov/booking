# Booking CRM

[//]: # ([Zherdesh-web workflow])
## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

[//]: # ([![Aiohttp]&#40;https://img.shields.io/badge/-Aiohttp-464646?style=flat-square&logo=Aiohttp&#41;]&#40;https://docs.aiohttp.org/&#41;)

[//]: # ([![Clickhouse]&#40;https://img.shields.io/badge/-Clickhouse-464646?style=flat-square&logo=Clickhouse&#41;]&#40;https://www.elastic.co/&#41;)

[//]: # ([![Elastic]&#40;https://img.shields.io/badge/-Elastic-464646?style=flat-square&logo=Elastic&#41;]&#40;https://clickhouse.com/&#41;)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Sentry](https://img.shields.io/badge/-Sentry-464646?style=flat-square&logo=Sentry)](https://sentry.io/)

[//]: # ([![MinIO]&#40;https://img.shields.io/badge/-MinIO-464646?style=flat-square&logo=MinIO&#41;]&#40;https://min.io/&#41;)

[//]: # ([![Selenium]&#40;https://img.shields.io/badge/-Selenium-464646?style=flat-square&logo=Selenium&#41;]&#40;https://www.selenium.dev/&#41;)

[//]: # ([![GitLab]&#40;https://img.shields.io/badge/-GitLab-464646?style=flat-square&logo=GitLab&#41;]&#40;https://gitlab.mplab.io/&#41;)
## Описание проекта
* Booking - Основная и самая важная часть платформы Booking CRM. 
## Доступ
* Актуальная версия: [^]($)
## Документация к API
* Документация к API можно посмотреть тут: \

[//]: # ([https://app.mamod.io/api/v1/docs/swagger/]&#40;https://app.mamod.io/api/v1/docs/swagger/&#41;)
* В локальной версии:
[http://127.0.0.1:8000/api/v1/docs/swagger/](http://127.0.0.1:8000/api/v1/docs/swagger/)

[//]: # (## Локальный запуск&#40;Фронтендерам&#41;)

[//]: # (* Устанавливаем Docker)

[//]: # (* Устанавливаем Docker compose)

[//]: # (* Клонируем репозиторий)

[//]: # (* Создаем файл .env в корне проекта)

[//]: # (* Копируем в него настройки из файла .env.example)

[//]: # ()
[//]: # (Меняем настройки для подключения к БД в файле .env на:)

[//]: # ()
[//]: # (* PG_NAME = test)

[//]: # (* PG_USER = test)

[//]: # (* PG_PASS = 1234)

[//]: # (* PG_HOST = database)

[//]: # (* PG_PORT = 5432)

[//]: # ()
[//]: # (Для запуска прописываем:)

[//]: # ()
[//]: # (```bash)

[//]: # (docker compose -f docker-compose.frontend.yml up --build)

[//]: # (```)

## Локальный запуск

### Клонирование репозитория 

Обратите внимание на точку вконце, это говорит о том чтобы скопировать в текущую директорию

```bash
git clone https://github.com/Sino0on/booking .
```

### Создание БД PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE USER name_user WITH PASSWORD 'password';
CREATE DATABASE name_db WITH OWNER name_user;
```

### Виртуальное окружение

```bash 
python3.10 -m venv venv &&
source venv/bin/activate &&
pip install -U pip &&
pip install -r requirements/dev.txt
```

> В Windows меняем строчку source venv/bin/activate на .\venv\Scripts\activate

> На продакшене меняем последнюю строчку на pip install -r requirements/prod.txt 

### Настройки окружения

1. Создаем файл .env в корне проекта
2. Копируем в него настройки из файла .env.example
3. Прописываем в нем свои значения

## Работа с репозиторием

### Установка новых зависимостей

При добавлении новых зависимостей нужно четко ответить себе на вопросы:
1. Является ли зависимость только для dev-а? 
2. Является ли зависимость только для prod-а?
3. Нужна ли она и там и там?

Допустим REQUIREMENT = название зависимости, которую мы хотим установить

```bash
pip install REQUIREMENT && pip freeze | grep REQUIREMENT >> requirements/dev.txt
```

Если в production, то в конце прописать prod.txt, вместо dev.txt

Если нужно и там и там, то:

```bash
pip install REQUIREMENT && 
pip freeze | grep REQUIREMENT >> requirements/dev.txt && 
pip freeze | grep REQUIREMENT >> requirements/prod.txt
```

### Настройки django

Файлы настроек:
* core/settings/base_settings - **Базовые** настройки
* core/settings/prod_settings - **Production** настройки
* core/settinng/dev_settings - **Development** настройки

Когда нам нужно добавить или изменить что-то в настройках мы должны сделать это в файле dev и в файле prod таким образом, чтобы обеспечить независимую работу как локально так и на проде

Когда настройка одинаковая и на dev и на prod, то мы добавляем ее только в Базовые настройки(base_settings)

#### Импорт настроек в коде

Пример НЕ **ПРАВИЛЬНОГО** импорта:

``` python
from core.settings.prod_settings import CSRF_TRUSTED_ORIGINS
```

Пример **ПРАВИЛЬНОГО** импорта:

```python
from django.conf import settings


CSRF_TRUSTED_ORIGINS = settings.CSRF_TRUSTED_ORIGINS
```

Это важно ведь в первом случае мы указываем какой файл настроек использовать, а во втором мы говорим джанго использовать те настройки, на которых он был запущен

## Code-base structure(Не актуально/обновляется)

The project is coded using a simple and intuitive structure presented bellow:

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app configuration
   |    |-- settings.py                    # Defines Global Settings
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- views.py                  # Serve HTML pages for authenticated users
   |    |    |-- urls.py                   # Define some super simple routes  
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- urls.py                   # Define authentication routes  
   |    |    |-- views.py                  # Handles login and registration  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                   # Master pages
   |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |         |    |-- base.html             # Used by common pages
   |         |
   |         |-- accounts/                  # Authentication pages
   |         |    |-- login.html            # Login page
   |         |    |-- register.html         # Register page
   |         |
   |         |-- home/                      # UI Kit Pages
   |              |-- index.html            # Index page
   |              |-- 404-page.html         # 404 page
   |              |-- *.html                # All other pages
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- manage.py                            # Start the app - Django default start script
   |
   |-- ************************************************************************
```
