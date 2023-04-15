[![Django-app workflow](https://github.com/Abdula-Dukuzov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Abdula-Dukuzov/yamdb_final/actions/workflows/yamdb_workflow.yml)

Описание YaMDb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles)

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Установка
Как скачать проект:
Клонируйте репозиторий и перейдите в него из командной строки:

git clone git@github.com:Abdula-Dukuzov/yamdb_final.git

Создание и наполнение env-файла /infra/.env
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql DB_NAME= postgres # задаем имя базы данных POSTGRES_USER= # задаем логин для подключения к базе данных POSTGRES_PASSWORD= # задаем пароль для подключения к БД DB_HOST=db # задаем название сервиса (контейнера) DB_PORT=5432 # порт для подключения к БД

Запуск контейнеров
В директории /infra/ выполните команду:

docker-compose up -d

Миграции, админка и база данных
Выполните команды:

docker-compose exec web python manage.py migrate docker-compose exec web python manage.py createsuperuser docker-compose exec web python manage.py collectstatic --noinput ```docker-compose exec web python manage.py loaddata fixtures.json``

Доступ к проекту
Проект доступен по адресу:

http://158.160.29.40

Технологии
Python 3.7.0
Django 2.2
Django REST framework
NGINX
Docker