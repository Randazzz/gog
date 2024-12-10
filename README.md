# Grace of the Gods (GOG)
Это проект интернет-магазина одежды Grace of the Gods, разработанный на Django. Он предоставляет пользователям удобный интерфейс для покупок одежды с различными функциональными возможностями.

## Содержание
- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка](#установка)
- [Запуск Development сервера](#запуск-development-сервера)
- [Тестирование](#тестирование)
- [Deploy](#deploy)
- [Зачем я разработал этот проект?](#зачем-я-разработал-этот-проект)

## Технологии
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Celery](https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Stripe](https://stripe.com/)

## Функциональность
- Регистрация и авторизация
- Аутентификация и восстановление пароля
- Подтверждение электронной почты
- Авторизация через сторонние сервисы
- Просмотр и фильтрация товаров по категориям
- Пагинация для удобного просмотра
- Добавление товаров в корзину и оформление заказа
- Редактирование данных пользователя

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/Randazzz/gog
    ```
2. Перейдите в директорию проекта:
    ```sh
    cd gog
    ```
3. Установите виртуальное окружение:
    ```sh
    python -m venv venv
    ```
4. Активируйте виртуальное окружение:
   - На Windows:
    ```sh
    venv\Scripts\activate
    ```
   - На macOS/Linux:
    ```sh
    source venv/bin/activate
    ```
5. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```
6. Напишите .env со всеми нужными настройками:
    ```
    DEBUG=True,
    SECRET_KEY=str,
    DOMAIN_NAME=str,

    REDIS_HOST=str,
    REDIS_PORT=int,

    DATABASE_NAME=str,
    DATABASE_USER=str,
    DATABASE_PASSWORD=str,
    DATABASE_HOST=str,
    DATABASE_PORT=int,

    EMAIL_HOST=str,
    EMAIL_PORT=int,
    EMAIL_HOST_USER=str,
    EMAIL_HOST_PASSWORD=str,
    EMAIL_USE_SSL=bool,
    DEFAULT_FROM_EMAIL=str,

    STRIPE_PUBLIC_KEY=str,
    STRIPE_SECRET_KEY=str,
    STRIPE_WEBHOOK_SECRET=str,
    ```

7. Запустите миграции:
    ```sh
    python manage.py migrate
    ```
8. Запустите Celery:
    ```sh
    celery -A gog worker -l INFO -P solo
    ```
9. Установка Stripe:

    Скачайте и установите Stripe CLI с официального сайта. Убедитесь, что он доступен в вашем PATH, чтобы можно было использовать команду stripe.

10. После установки Stripe запустите команду для прослушивания вебхуков:
    ```sh
    stripe listen --forward-to localhost:8000/stripe/webhook/
    ```


## Запуск Development сервера
Чтобы запустить сервер для разработки, выполните команду:

    python manage.py runserver


## Тестирование
Наш проект покрыт юнит-тестами. Для их запуска выполните команду:

    python manage.py test


## Deploy

    docker-compose up


### Зачем я разработал этот проект?
Проект был разработан как первый pet проект, для опыта
