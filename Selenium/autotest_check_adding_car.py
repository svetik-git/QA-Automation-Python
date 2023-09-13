import requests

from API.models import RegisterUser
from Selenium.hillel_auto_website import HillelAutoWebsite


class TestAddingCar:
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

    def test_check_functionality_adding_car(self):
        # Adding a car in the users garage
        hillel_auto = HillelAutoWebsite()
        hillel_auto.open_main_page()
        hillel_auto.login_page(self.email, self.password)
        hillel_auto.add_car_to_garage("BMW", "5", 100)
        hillel_auto.is_car_in_garage("BMW", "5")

        self.check_car_api()

    def check_car_api(self):
        signin_body = {
            "email": self.email,
            "password": self.password,
            "remember": True
        }
        session = requests.session()
        response = session.post(url="https://qauto2.forstudy.space/api/auth/signin", json=signin_body)
        assert response.json()["status"] == "ok"
        assert response.status_code == 200

        response = session.get(url="https://qauto2.forstudy.space/api/cars")
        assert response.json()["status"] == "ok"
        assert response.status_code == 200
        data = response.json()["data"]
        found = False
        for item in data:
            car_name = item["brand"]
            car_model = item["model"]
            if car_name == "BMW" and car_model == "5":
                found = True
                break
        assert found == True

    def teardown_class(self):
        print("teardown_class")
