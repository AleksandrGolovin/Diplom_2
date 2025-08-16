import allure
from data import ERROR_MESSAGES


@allure.title('Тесты логина пользователя')
class TestUserLogin:
    @allure.title('Логин пользователя с корректными учетными данными')
    @allure.description('Зарегистрировать пользователя, залогиниться пользователем, проверить код ответа, статус и наличие accessToken')
    def test_login_user_valid_credentials_success(self, create_user, user_methods):
        user_data = create_user()
        
        response = user_methods.login_user(user_data["email"], user_data["password"])
        response_json = response.json()
        
        assert all([
            response.status_code == 200,
            response_json["success"] is True,
            "accessToken" in response_json
        ])
    
    @allure.title('Логин пользователя с некорректными учетными данными')
    @allure.description('Зарегистрировать пользователя, залогиниться пользователем с неверным паролем, проверить код ответа, статус и текст ошибки')
    def test_login_user_invalid_credentials_failure(self, create_user, user_methods):
        user_data = create_user()
        
        response = user_methods.login_user(user_data["email"], "wrong_password")
        response_json = response.json()
        
        assert all([
            response.status_code == 401,
            response_json["success"] is False,
            response_json["message"] == ERROR_MESSAGES["invalid_credentials"]
        ])
