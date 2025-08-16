import requests
import allure


class UserMethods:
    def __init__(self, namespace_url):
        self.namespace_url = namespace_url

    @allure.step('Регистрация пользователя (POST)')
    def register_user(self, *args):
        # Перегрузка аргументов
        match args:
            # На входе email, password, name
            case (str(email), str(password), str(name)):
                payload = {
                    "email": email,
                    "password": password,
                    "name": name
                }
            # На входе готовый словарь для payload
            case (dict(data),):
                payload = data
            case _:
                raise TypeError("Неподдерживаемые аргументы")
        response = requests.post(
            url=f'{self.namespace_url}/register',
            json=payload
        )
        return response

    @allure.step('Обновление данных пользователя (PATCH)')
    def update_user(self, access_token=None, payload={}):
        headers = {"Authorization": f"{access_token}"} if access_token else None
        response = requests.patch(
            url=f'{self.namespace_url}/user',
            headers=headers,
            json=payload
        )
        return response
    
    @allure.step('Удаление пользователя (DELETE)')
    def delete_user(self, access_token=None):
        headers = {"Authorization": f"{access_token}"} if access_token else None
        response = requests.delete(
            url=f'{self.namespace_url}/user',
            headers=headers
        )
        return response
    
    @allure.step('Логин пользователя (POST)')
    def login_user(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(
            url=f'{self.namespace_url}/login',
            json=payload
        )
        return response
