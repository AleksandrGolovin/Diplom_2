import pytest
import allure
from data import ERROR_MESSAGES


@allure.title('Тесты регистрации пользователя')
class TestUserRegistration:
    @allure.title('Регистрация пользователя с уникальными учетными данными')
    @allure.description('Зарегистрировать пользователя, проверить код ответа, статус и наличие accessToken')
    def test_create_unique_user(self, create_user):
        user_data = create_user()
        response = user_data["response"]
        response_json = response.json()

        assert all([
            response.status_code == 200,
            response_json["success"] is True,
            "accessToken" in response_json
        ])

    @allure.title('Регистрация пользователя с неуникальными учетными данными (пользователь с таким email уже есть)')
    @allure.description('Зарегистрировать Пользователя-1 с уникальными учетными данными, зарегистрировать Пользователя-2 с e-mail Пользователя-1, проверить код ответа, статус и текст ошибки')
    def test_create_existing_user(self, create_user):
        first_user = create_user()
        
        second_user = create_user(
            email=first_user["email"],
            password="different_password",
            name="Different Name"
        )
        response = second_user['response']
        response_json = response.json()

        assert all([
            response.status_code == 403,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["user_exists"]
        ])

    @allure.title('Регистрация пользователя с неполными учетными данными')
    @allure.description('Параметризацией выбрать пропускаемое поле, зарегистрировать пользователя, проверить код ответа, статус и тект ошибки')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field, user_methods):
        payload = {
            "email": "test@example.com",
            "password": "password",
            "name": "Test User"
        }
        payload.pop(missing_field)
        
        response = user_methods.register_user(payload)
        response_json = response.json()

        assert all([
            response.status_code == 403,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["required_fields"]
        ])
