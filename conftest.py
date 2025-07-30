import pytest
from helpers import generate_unique_email
from data import DEFAULT_PASSWORD, BASE_URL
from methods.user_methods import UserMethods
from methods.orders_methods import OrdersMethods
from methods.ingredients_methods import IngredientsMethods


@pytest.fixture
def user_methods() -> UserMethods:
    """
    Методы пользователя:
    - register_user(*args)
    - update_user(access_token=None, payload={})
    - delete_user(access_token=None)
    - login_user(email, password)
    """
    user_url = f'{BASE_URL}/auth'
    user_methods = UserMethods(user_url)
    return user_methods

@pytest.fixture
def orders_methods() -> OrdersMethods:
    """
    Методы заказов:
    - create_order(access_token = None, ingredients: list[str] = [])
    - get_orders(access_token = None)
    """
    orders_methods = f'{BASE_URL}/orders'
    orders_methods = OrdersMethods(orders_methods)
    return orders_methods

@pytest.fixture(scope="session")
def ingredients_methods() -> IngredientsMethods:
    """
    Методы ингредиентов:
    - get_ingredients()
    """
    ingredients_url = f'{BASE_URL}/ingredients'
    ingredients_methods = IngredientsMethods(ingredients_url)
    return ingredients_methods

@pytest.fixture(scope="session")
def valid_ingredients_id(ingredients_methods) -> list[str]:
    """
    Валидный список ID (хэшей) ингредиентов
    """
    response = ingredients_methods.get_ingredients()
    return [ingredient["_id"] for ingredient in response.json()["data"]]

@pytest.fixture
def create_user(user_methods):
    """
    Фикстура для создания пользователя и его последующего удаления
    """
    users_to_delete = []

    def _create_user(email=None, password=None, name=None):
        # Получаем или генерируем данные пользователя
        email = email or generate_unique_email()
        password = password or DEFAULT_PASSWORD
        name = name or "Test User"

        # Делаем запрос на создание
        register_response = user_methods.register_user(email, password, name)

        # Сохраняем учетные данные для последующего удаления пользователя
        users_to_delete.append((email, password))

        return {
            "response": register_response,
            "email": email,
            "password": password,
            "name": name
        }
    
    yield _create_user
    
    # Удаляем пользователей после выполнения тестов
    for email, password in users_to_delete:
        login_response = user_methods.login_user(email, password)
        if login_response.status_code == 200:
            token = login_response.json()["accessToken"]
            user_methods.delete_user(token)

@pytest.fixture
def auth_user(create_user, user_methods):
    """
    Фикстура для создания, авторизации и удаления пользователя
    """
    def _auth_user():
        # Создаем пользователя
        user_data = create_user()
        
        # Авторизуем пользователя
        login_response = user_methods.login_user(user_data["email"], user_data["password"])
        
        return {
            "response": login_response,
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"]
        }
    
    return _auth_user
