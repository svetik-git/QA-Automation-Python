import time

from selenium import webdriver
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class HillelAutoWebsite:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    def open_main_page(self):
        self.driver.get("https://guest:welcome2qauto@qauto2.forstudy.space/")

    def login_page(self, email: str, password: str):
        # Login on site
        signin_button = self.driver.find_element(By.XPATH,
                                                 "/html/body/app-root/app-global-layout/div/div/app-header/header/div/div/div[2]/button[2]")
        assert signin_button is not None
        signin_button.click()
        email_input = self.driver.find_element(By.ID, "signinEmail")
        email_input.clear()
        email_input.send_keys(email)
        password_input = self.driver.find_element(By.ID, "signinPassword")
        password_input.clear()
        password_input.send_keys(password)
        login_button = self.driver.find_element(By.XPATH,
                                                "/html/body/ngb-modal-window/div/div/app-signin-modal/div[3]/button[2]")
        assert login_button is not None
        login_button.click()
        time.sleep(3)

    def add_car_to_garage(self, brand: str, model: str, mileage: int):
        # Add a car in garage
        add_car_button = self.driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        add_car_button.click()
        time.sleep(2)

        modal_content = self.driver.find_element(By.CLASS_NAME, "modal-content")
        brand_input = Select(modal_content.find_element(By.ID, "addCarBrand"))
        brand_input.select_by_visible_text(brand)
        # brand_input.select_by_index(1)
        # brand_input.select_by_value("1: 2")
        time.sleep(2)

        model_input = Select(modal_content.find_element(By.ID, "addCarModel"))
        model_input.select_by_visible_text(model)
        # model_input.select_by_index(1)
        # model_input.select_by_value("6: 7")
        time.sleep(2)

        mileage_input = modal_content.find_element(By.ID, "addCarMileage")
        mileage_input.send_keys(mileage)
        time.sleep(2)

        add_button = modal_content.find_element(By.CSS_SELECTOR, ".btn.btn-primary")
        add_button.click()

    def is_car_in_garage(self, brand: str, model: str):
        # Check car in garage
        car_list = self.driver.find_element(By.CLASS_NAME, "car-list")
        car_items = car_list.find_elements(By.CLASS_NAME, "car-item")

        found = False
        for item in car_items:
            car_name = item.find_element(By.CSS_SELECTOR, ".car_name.h2")
            if car_name.text == f"{brand} {model}":
                found = True
                break
        assert found == True
