import allure
from data import ERROR_MESSAGES


@allure.title('Тесты создания заказов')
class TestOrderCreation:
    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description('Создать и авторизоваться пользователем, получить валидные ID ингредиентов, создать заказ, проверить код ответа, статус и наличие номера заказа')
    def test_create_order_authenticated(self, auth_user, orders_methods, valid_ingredients_id):
        user_data = auth_user()
        access_token = user_data['response'].json()['accessToken']
        ingredients = valid_ingredients_id[:2]
        
        response = orders_methods.create_order(access_token, ingredients)
        response_json = response.json()
        
        assert all([
            response.status_code == 200,
            response_json["success"] is True,
            "number" in response_json["order"]
        ])
    
    @allure.title('Создание заказа неавторизованным пользователем (ОШИБКА В ДОКУМЕНТАЦИИ: ОЖИДАНИЕ - ОШИБКА, ФАКТ - УСПЕХ)')
    @allure.description('Получить валидные ID ингредиентов, создать заказ, проверить код ответа')
    def test_create_order_unauthenticated(self, orders_methods, valid_ingredients_id):
        ingredients = valid_ingredients_id[:2]
        
        response = orders_methods.create_order(ingredients=ingredients)
        
        assert response.status_code == 200  # Ошибка в документации, ожидание - 401
    
    @allure.title('Создание заказа авторизованным пользователем без указания ингредиентов')
    @allure.description('Создать и авторизоваться пользователем, получить валидные ID ингредиентов, создать заказ без ингредиентов, проверить код ответа, статус и текст ошибки')
    def test_create_order_no_ingredients(self, auth_user, orders_methods):
        user_data = auth_user()
        access_token = user_data['response'].json()['accessToken']
        
        response = orders_methods.create_order(access_token)
        response_json = response.json()
        
        assert all([
            response.status_code == 400,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["missing_ingredients"]
        ])
    
    @allure.title('Создание заказа авторизованным пользователем с невалидным ингредиентом')
    @allure.description('Создать и авторизоваться пользователем, создать заказ с невалидным ингредиентом, проверить код ответа')
    def test_create_order_invalid_hash(self, auth_user, orders_methods):
        user_data = auth_user()
        access_token = user_data['response'].json()['accessToken']
        
        response = orders_methods.create_order(access_token, ['invalid_ingredient_id'])

        assert response.status_code == 500
