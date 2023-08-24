import requests

from API.models import RegisterUser


class TestCreateUser:
    def setup_class(self):
        random_data = RegisterUser.random()
        self.email = random_data["email"]
        self.password = random_data["password"]

    def test_signup_failed(self):
        failed_signup_body = {
            "name": "John",
            "lastName": "Dou",
            "email": self.email,
            "password": self.password,
            "repeatPassword": "Qwerty"
        }
        response = requests.post(url="https://qauto2.forstudy.space/api/auth/signup", json=failed_signup_body)
        assert response.json()["status"] == "error"
        assert response.status_code == 400

    def test_signup_success(self):
        signup_body = {
            "name": "John",
            "lastName": "Dou",
            "email": self.email,
            "password": self.password,
            "repeatPassword": self.password
        }
        response = requests.post(url="https://qauto2.forstudy.space/api/auth/signup", json=signup_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 201

        signin_body = {
            "email": self.email,
            "password": self.password,
            "remember": True
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=signin_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

        response = session.delete(url="https://qauto2.forstudy.space/api/users")
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

