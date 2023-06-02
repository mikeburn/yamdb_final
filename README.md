![Yamdb Workflow Status](https://github.com/saylanm/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# ЯП - Спринт 16 - CI и CD проекта api_yamdb. Python-разработчик (бекенд) (Яндекс.Практикум)

## 1. О проекте:
YaMDb - проект для публикации отзывов о различных произведениях интеллектуальной собственности (фильмы, книги, музыка и проч) 

API  позволяет взаимодействовать с проектом YaMDb посредством отправки запросов на URL интерфейса.

## 2. Авторы проекта:
- Семён Семёнов - https://github.com/saylanm

## 3. Используемые технологии:
- Django 3.2
- Django REST Framework 3.12.4
- Django REST Framework Simple JWT 4.8.0
- Библиотека csv для возможности импорта в Базу данных

## 4. Как запустить проект:

Все описанное ниже относится к ОС Linux.

Клонируем репозиторий и переходим в него:

```bash
git clone git@github.com:saylanm/infra_sp2.git
cd infra_sp2/
cd infra/
```

Поднимаем контейнеры:

```bash
docker-compose up -d --build
```

Выполняем миграции:

```bash
docker-compose exec web python manage.py makemigrations reviews
```

```bash
docker-compose exec web python manage.py migrate
```

Создаем суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

Собираем статику:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

Создаём дамп базы данных (нет в текущем репозитории):

```bash
docker-compose exec web python manage.py dumpdata > dumpPostrgeSQL.json
```

Останавливаем контейнеры:

```bash
docker-compose down -v
```

### Шаблон наполнения .env (не включен в текущий репозиторий) расположенный по пути infra/.env

```
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default=5432)
    }
}
```

## 5. Примеры запросов:
### Создание пользователя и получение JWT-токена для него
Для создания пользователя необходимо отправить запрос на эндпоинт:
```
http://158.160.2.78/api/v1/auth/signup/
```
Пример запроса:
```json
{
    "username": "ivan",
    "email": "ivan@yandex.ru"
}
```
На указанный адрес электронной почты будет отправлен четырехзначный код подтверждения (в данном проекте не подключен smtp-сервер - отправка письма осуществляется путем эмуляции почтового сервера средствами Django, письма сохраняются в каталог `sent_mails`)

Для последующего получения токена необходимо оправить запрос с `username` пользователя и `confirmation_code` на эндпоинт:
```
http://158.160.2.78/api/v1/auth/token/
```
Пример запроса:
```json
{
    "username": "ivan",
    "confirmation_code": 3364
}
```
В ответ на указанный запрос будет возвращен JWT-токен
## 6. Подробная документация по API:
Доступна после запуска проекта - см. п.4:
#### Документцаю можно открыть по ссылке:
```http://158.160.2.78/redoc/```
#### Проект размещен по ссылке:
```http://158.160.2.78```

## 7. Импорт данных из csv-файлов
Разместить в каталоге проекта `static/data/` csv-файлы, соответствующие названиям моделей.
Например static/data/category.csv

Ввести в консоли:
```bash
python manage.py import_cvs
```