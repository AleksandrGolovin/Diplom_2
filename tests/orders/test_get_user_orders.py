import allure
from data import ERROR_MESSAGES


@allure.title('Тесты заказов пользователя')
class TestUserOrders:
    @allure.title('Получить заказы авторизованного пользователя')
    @allure.description('Создать и авторизоваться пользователем, получить валидные ID ингредиентов, создать заказ, получить список заказов пользователя, проверить код ответа, статус и сверить номер заказа')
    def test_get_orders_authorized_success(self, auth_user, orders_methods, valid_ingredients_id):
        user_data = auth_user()
        access_token = user_data['response'].json()['accessToken']
        ingredients = valid_ingredients_id[:2]
        response = orders_methods.create_order(access_token, ingredients)
        order_number = response.json()['order']['number']
        
        response = orders_methods.get_orders(access_token)
        response_json = response.json()
        
        assert all([
            response.status_code == 200,
            response_json["success"] is True,
            response_json['orders'][0]['number'] == order_number
        ])
    
    @allure.title('Получить заказы неавторизованного пользователя')
    @allure.description('Получить список заказов без авторизации, проверить код ответа, статус и текст ошибки')
    def test_get_orders_unauthorized_failure(self, orders_methods):
        response = orders_methods.get_orders()
        response_json = response.json()
        
        assert all([
            response.status_code == 401,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["unauthorized"]
        ])
