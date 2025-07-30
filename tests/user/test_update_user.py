import allure
from helpers import generate_unique_email
from data import ERROR_MESSAGES


@allure.title('Тесты обновления пользовательских учетных данных')
class TestUserUpdate:
    @allure.title('Обновить пользовательские данные авторизованного пользователя')
    @allure.description('Создать и авторизоваться пользователем, отправить корректные обновленные данные, проверить код ответа, статус, сверить учетные данные из ответа')
    def test_update_authorized(self, auth_user, user_methods):
        user_data = auth_user()
        access_token = user_data['response'].json()['accessToken']
        payload = {
            "email": generate_unique_email(),
            "name": "Updated Name",
            "password": "Updated Password"
        }

        response = user_methods.update_user(access_token, payload)
        response_json = response.json()
        
        assert all([
            response.status_code == 200,
            response_json["success"] is True,
            response_json["user"]["email"] == payload["email"],
            response_json["user"]["name"] == payload["name"]
        ])
    
    @allure.title('Обновить пользовательские данные неавторизованного пользователя')
    @allure.description('Отправить корректные обновленные данные (имя) без авторизации, проверить код ответа, статус и текст ошибки')
    def test_update_unauthorized(self, user_methods):
        payload = {"name": "Should Fail"}

        response = user_methods.update_user(payload=payload)
        response_json = response.json()

        assert all([
            response.status_code == 401,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["unauthorized"]
        ])
