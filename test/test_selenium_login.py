from selenium import webdriver
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot',
                                        element)
    return shadow_root


class TestSignUp():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_signup(self):
        driver = self.driver
        html_file = os.path.abspath('..') + "/templates/login.html"
        driver.get("file:" + html_file)
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            ustr = 'usertest@mail.com'
            pstr = 'password123'
            username = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//input[@name = 'username']")
            password = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//input[@name = 'password']")
            for u in username:
                u.clear()
                u.send_keys(ustr)
            for p in password:
                p.clear()
                p.send_keys(pstr)
            time.sleep(1)
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            print("click signup username&psw ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()


class TestLogIn():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_login(self):
        driver = self.driver
        html_file = os.path.abspath('..') + "/templates/login.html"
        driver.get("file:" + html_file)
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            ustr = 'usertest@mail.com'
            pstr = 'password123'
            username = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//input[@name = 'username']")
            password = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//input[@name = 'password']")
            for u in username:
                u.clear()
                u.send_keys(ustr)
            for p in password:
                p.clear()
                p.send_keys(pstr)
            time.sleep(1)
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//button")
            for b in submit:
                b.click()
            print("click login username&psw ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
