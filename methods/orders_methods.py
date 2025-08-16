import requests
import allure


class OrdersMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url
    
    @allure.step('Создание заказа (POST)')
    def create_order(self, access_token = None, ingredients: list[str] = []):
        headers = {"Authorization": f"{access_token}"} if access_token else None
        response = requests.post(
            f"{self.namespace_url}",
            headers=headers,
            json={"ingredients": ingredients}
        )
        return response
    
    @allure.step('Получить заказы пользователя (GET)')
    def get_orders(self, access_token = None):
        headers = {"Authorization": f"{access_token}"} if access_token else None
        response = requests.get(
            f"{self.namespace_url}",
            headers=headers
        )
        return response
