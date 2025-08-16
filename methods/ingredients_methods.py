import requests
import allure


class IngredientsMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url
    
    @allure.step('Получить список доступных ингредиентов (GET)')
    def get_ingredients(self):
        response = requests.get(f"{self.namespace_url}")
        return response
