from selenium import webdriver
# import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import app
import multiprocessing

options = webdriver.ChromeOptions()
options.add_argument('-headless')


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot',
                                        element)
    return shadow_root


def run_server():
    app.app.run()


class TestSignUp():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_signup(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            ustr = 'usersignup@mail.com'
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
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            try:
                WebDriverWait(driver, 3).until(  # waitforhabitpage
                    EC.presence_of_element_located((By.CLASS_NAME, "alert"))
                )
            except TimeoutException:
                print("signup success")
            else:
                assert False, ("signup fail")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()


class TestSignUpFail():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_signup_fail(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            ustr = 'repeatuser@mail.com'
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
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)

            ustr = 'repeatuser@mail.com'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            try:
                WebDriverWait(driver, 3).until(  # waitforfailmessage
                    EC.presence_of_element_located((By.CLASS_NAME, "alert"))
                )
            except TimeoutException:
                assert False, ("repeated username signup success")
            finally:

                ustr = 'usertest@mail'
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

                submit = driver.find_elements_by_xpath(
                    "//div/div/div[@id = 'signup']//button")
                for b in submit:
                    b.click()
                time.sleep(1)

                try:
                    WebDriverWait(driver, 3).until(
                        # waitforfailmessage
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "alert"))
                    )
                except TimeoutException:
                    assert False, ("wrong email signup success")
                else:
                    print("signup fail ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()


class TestSignUpInvalidUsername():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_invalid_signup_email(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            ustr = 'usertest'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

            ustr = 'usertest@'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

            ustr = 'usertest@mail.'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()


class TestLogIn():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_login(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            ustr = 'userlogin@mail.com'
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
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'signup']//button")
            for b in submit:
                b.click()
            time.sleep(1)

            driver.find_element_by_link_text("Log In").click()

            ustr = 'userlogin@mail.com'
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
            time.sleep(1)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "zg-head-cell"))
                )
            except TimeoutException:
                assert False, ("login fail")
            else:
                print("login success")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()


class TestLoginInvalidUsername():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_invalid_login_email(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            driver.find_element_by_link_text("Log In").click()
            ustr = 'usertest'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

            ustr = 'usertest@'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

            ustr = 'usertest@mail.'
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

            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//button")
            for b in submit:
                b.click()
            time.sleep(1)
            for u in username:
                is_valid = driver.execute_script(
                    "return arguments[0].validity.valid", u)
                assert (not is_valid), "invalid email address message not show"

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()


class TestLogInFail():

    def setup_method(self, method):
        self.proc = multiprocessing.Process(target=run_server, args=())
        self.proc.start()
        self.driver = webdriver.Chrome(options=options)

    def test_login_fail(self):
        driver = self.driver
        # html_file = os.path.abspath('.') + "/templates/login.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            driver.find_element_by_link_text("Log In").click()
            ustr = 'neverregister@mail.com'
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
            submit = driver.find_elements_by_xpath(
                "//div/div/div[@id = 'login']//button")
            for b in submit:
                b.click()
            time.sleep(1)

            try:
                WebDriverWait(driver, 3).until(  # waitforfailmessage
                    EC.presence_of_element_located((By.CLASS_NAME, "alert"))
                )
            except TimeoutException:
                assert False, ("repeated username login success")
            finally:
                driver.find_element_by_link_text("Log In").click()
                ustr = 'usertest@mail'
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

                submit = driver.find_elements_by_xpath(
                    "//div/div/div[@id = 'login']//button")
                for b in submit:
                    b.click()
                time.sleep(1)

                try:
                    WebDriverWait(driver, 3).until(
                        # waitforfailmessage
                        EC.presence_of_element_located(
                            (By.CLASS_NAME, "alert"))
                    )
                except TimeoutException:
                    assert False, ("wrong email login success")
                else:
                    print("login fail ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()
        self.proc.terminate()
