import requests

from API.models import RegisterUser


class TestLoginUser:
    def setup_class(self):
        random_data = RegisterUser.random()
        self.email = random_data["email"]
        self.password = random_data["password"]

    def setup_method(self):
        # Registration user before every test:
        # Registration user
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
        print("setup_method")

    def teardown_method(self):
        # Delete user after every test:
        # Login user - login and password
        # Delete user
        signin_body = {
            "email": self.email,
            "password": self.password,
            "remember": False
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=signin_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

        response = session.delete(url="https://qauto2.forstudy.space/api/users")
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

    def test_signin_success(self):
        # Authenticates user:
        # Login user - login and password
        # Success login: status - ok, status code - 200
        signin_body = {
            "email": self.email,
            "password": self.password,
            "remember": False
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=signin_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

    def test_users_profile(self):
        # Gets authenticated user profile data:
        # Login user - login and password
        # Success login: status - ok, status code - 200
        # Check profile of user. Compare profile data and registration data
        signin_body = {
            "email": self.email,
            "password": self.password,
            "remember": True
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=signin_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

        response = session.get(url="https://qauto2.forstudy.space/api/users/profile")
        assert response.json()["status"] == "ok"
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "John"
        assert response.json()["data"]["lastName"] == "Dou"

    def test_signin_failed(self):
        # Login user - login and password
        # Failed login: status - error, status code - 400
        # Login user success

        failed_signin_body = {
            "email": self.email,
            "password": self.password + "$",
            "remember": False
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=failed_signin_body)
        assert response.json()["status"] == "error"
        assert response.status_code == 400

    def teardown_class(self):
        print("teardown_class")

