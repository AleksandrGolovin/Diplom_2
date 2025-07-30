# Diplom_2: Stellar Burgers API Testing

## Описание проекта
Проект представляет собой автоматизированные тесты API для сервиса **Stellar Burgers**. Тесты охватывают ключевые функции системы:
- Регистрация и авторизация пользователей
- Обновление и удаление профиля
- Формирование заказов
- Работа с ингредиентами
- Получение истории заказов

Тесты реализованы на Python с использованием:
- `pytest` для организации тестов
- `requests` для HTTP-запросов
- `allure` для формирования отчетов
- Параметризация тестов для проверки граничных случаев

## Тестовые классы и методы

### test_register_user.py
**Класс**: TestUserRegistration  
Тесты регистрации новых пользователей:

- test_register_user_unique_success:  
  Регистрация с валидными уникальными данными
- test_register_user_existing_failure:  
  Регистрация с email существующего пользователя (ожидается ошибка 403)
- test_register_user_missing_field_failure:  
  Регистрация без обязательных полей (email/password/name)

### test_login_user.py
**Класс**: TestUserLogin  
Тесты авторизации пользователей:

- test_login_user_valid_credentials_success:  
  Вход с корректными email и паролем
- test_login_user_invalid_credentials_failure:  
  Вход с неверным паролем (ожидается 401)

### test_update_user.py
**Класс**: TestUserUpdate  
Тесты обновления данных профиля:

- test_update_user_authorized_success:  
  Обновление данных с валидным токеном авторизации
- test_update_user_unauthorized_failure:  
  Обновление данных без авторизации (ожидается 401)

### test_create_order.py
**Класс**: TestOrderCreation  
Тесты создания заказов:

- test_create_order_authorized_success:  
  Создание заказа с валидными ингредиентами (авторизованный пользователь)
- test_create_order_unauthorized_failure:  
  Создание заказа без авторизации (текущая реализация API разрешает это)
- test_create_order_no_ingredients_failure:  
  Создание заказа без ингредиентов (ожидается ошибка 400)
- test_create_order_invalid_hash_failure:  
  Создание заказа с несуществующим ингредиентом (ожидается ошибка 500)

### test_get_user_orders.py
**Класс**: TestUserOrders  
Тесты получения истории заказов:

- test_get_orders_authorized_success:  
  Получение заказов авторизованного пользователя
- test_get_orders_unauthorized_failure:  
  Получение заказов без авторизации (ожидается ошибка 401)

## Установка и запуск

### Установка зависимостей
Установите необходимые пакеты из файла `requirements.txt` командой:  
> `pip install -r requirements.txt`

### Запуск тестов
Выполните команду:  
> `pytest --alluredir=allure_results`

### Просмотр отчета Allure
1. Запустите сервер с отчетом:  
> `allure serve allure_results`

2. Для генерации статического отчета:  
> `allure generate allure_results -o allure_report --clean`

После этого откройте файл `allure_report/index.html` в браузере.

## Структура проекта
Основные компоненты проекта:
- `conftest.py`: Фикстуры для подготовки тестовых данных
- `data.py`: Конфигурация API и сообщения об ошибках
- `helpers.py`: Утилиты для генерации тестовых данных
- `methods/`: Реализация API-методов
- `tests/`: Наборы тестовых сценариев

Тесты проверяют как позитивные сценарии работы API, так и обработку ошибок в соответствии с документацией системы.