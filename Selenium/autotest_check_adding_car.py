import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from API.models import RegisterUser


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
        # Adding a car in the users garage:
        # Login using Selenium
        # Add a car using Selenium
        # Check car in garage using Selenium and API
        # Teardown all data

        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)
        driver.get("https://guest:welcome2qauto@qauto2.forstudy.space/")

        signin_button = driver.find_element(By.XPATH,
                                            "/html/body/app-root/app-global-layout/div/div/app-header/header/div/div/div[2]/button[2]")
        assert signin_button is not None
        signin_button.click()
        email_input = driver.find_element(By.ID, "signinEmail")
        email_input.clear()
        email_input.send_keys(self.email)
        password_input = driver.find_element(By.ID, "signinPassword")
        password_input.clear()
        password_input.send_keys(self.password)
        login_button = driver.find_element(By.XPATH,
                                           "/html/body/ngb-modal-window/div/div/app-signin-modal/div[3]/button[2]")
        assert login_button is not None
        login_button.click()

        time.sleep(3)

        add_car_button = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        add_car_button.click()

        time.sleep(2)
        modal_content = driver.find_element(By.CLASS_NAME, "modal-content")
        brand_input = Select(modal_content.find_element(By.ID, "addCarBrand"))
        brand_input.select_by_index(1)
        time.sleep(1)
        model_input = Select(modal_content.find_element(By.ID, "addCarModel"))
        model_input.select_by_index(1)
        mileage_input = modal_content.find_element(By.ID, "addCarMileage")
        mileage_input.send_keys("100")
        add_button = modal_content.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        add_button.click()

        car_list = driver.find_element(By.CLASS_NAME, "car-list")
        car_items = car_list.find_elements(By.CLASS_NAME, "car-item")

        found = False
        for item in car_items:
            car_name = item.find_element(By.CSS_SELECTOR, ".car_name.h2")
            if car_name.text == "BMW 5":
                found = True
                break
        assert found == True
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

