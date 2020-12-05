import random
import string
from selenium import webdriver
import os
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class TestStreak():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_log_button_streak(self):
        driver = self.driver
        html_file = os.path.abspath(
            '..') + "/sandbox/grid_demo_habit_manager.html"
        driver.get("file:" + html_file)
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(  # waitforpage
                EC.presence_of_element_located((By.TAG_NAME, "zg-head-cell"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:

            log_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']")
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']/div")
            sl = []
            for streak in streak_list:
                sl.append(int(''.join(filter(str.isdigit, streak.text))))
            ssl = sl.copy()
            ssl.sort(reverse=True)
            assert sl == ssl, "Streak is not sorted"

            for button in log_button:
                # driver.execute_script("document.getElementsByClassName('log-button')[0].click()")
                driver.execute_script("arguments[0].click()", button)
                # checkstreaknotdoublecount
                driver.execute_script("arguments[0].click()", button)

            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']")
            for i, j in zip(sl, streak_list):
                # print(type(i))
                # print(int(''.join(filter(str.isdigit, j.text))))
                assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                    ), "wrong streak"
            print("log-button/streak ok")

            # elem = driver.find_element_by_name("q")
            # elem.send_keys("pycon")
            # elem.send_keys(Keys.RETURN)
            # assert "No results found." not in driver.page_source

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()


class TestDeleteHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_delete_button(self):
        driver = self.driver
        html_file = os.path.abspath(
            '..') + "/sandbox/grid_demo_habit_manager.html"
        driver.get("file:" + html_file)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "zg-head-cell"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            # log_button = driver.find_elements_by_class_name("log-button")
            remove_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@action = 'removerecord']")
            length = len(remove_button)
            tmp = length
            delete = driver.execute_script(
                'return document.querySelector("zg-dialog").shadowRoot.'
                'querySelector("button.zg-dialog-confirm")')
            if delete is None:
                print("null")

            for button in remove_button:
                driver.execute_script("arguments[0].click()", button)

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//zg-dialog[@open]"))
                    )
                except TimeoutException:
                    assert True, ("load slowly")
                else:
                    delete.click()
                    # checkfordeleteonerow
                    remain = driver.find_elements_by_xpath(
                        "//zing-grid/zg-body/zg-row[@hidden]")
                    assert (tmp - 1) == (length-len(remain)), "Wrong delete"
                    tmp = tmp - 1

            print("delete habit ok")

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()


class TestLogDelete():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_log_button_streak(self):
        driver = self.driver
        html_file = os.path.abspath(
            '..') + "/sandbox/grid_demo_habit_manager.html"
        driver.get("file:" + html_file)
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "zg-head-cell"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            # log_button = driver.find_elements_by_class_name("log-button")
            log_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']")
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']/div")
            sl = []

            remove_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@action = 'removerecord']")
            length = len(remove_button)
            tmp = length
            delete = driver.execute_script(
                'return document.querySelector("zg-dialog").shadowRoot.'
                'querySelector("button.zg-dialog-confirm")')
            if delete is None:
                print("null")

            for streak in streak_list:
                sl.append(int(''.join(filter(str.isdigit, streak.text))))
            # driver.find_element_by_xpath("//form[@id='loginForm']")
            for lg, d, s in zip(log_button, remove_button, sl):

                driver.execute_script("arguments[0].click()", lg)  # log
                st = driver.find_element_by_xpath(
                    "//zg-body//zg-cell[@data-field-index='streak']")
                assert (s+1) == int(''.join(filter(str.isdigit, st.text))
                                    ), "wrong streak"   # streak
                # disable log button
                assert 1 == len(driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@class = 'log-button' "
                    "and @disabled]")), "log button still work"

                driver.execute_script("arguments[0].click()", d)  # delete
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//zg-dialog[@open]"))
                    )
                except TimeoutException:
                    assert True, ("load slowly")
                else:
                    time.sleep(1)
                    delete.click()
                    print('delete row{}'.format(
                        len(driver.find_elements_by_xpath(
                            "//zing-grid/zg-body/zg-row[@hidden]"))))
                    assert (length-len(driver.find_elements_by_xpath(
                        "//zing-grid/zg-body/zg-row"
                        "[@hidden]"))) == tmp - 1, "Wrong delete"
                    # time.sleep(5)
                    tmp = tmp - 1

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()


class TestCreateHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_create(self):
        driver = self.driver
        html_file = os.path.abspath(
            '..') + "/sandbox/grid_demo_habit_manager.html"
        driver.get("file:" + html_file)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "zg-head-cell"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            new_habit = driver.find_element_by_xpath(
                "//input[@id ='new-habit']")
            create = driver.find_element_by_xpath("//button[@id ='add']")
            ct = len(driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']"))
            for i in range(1, 10):
                habit = get_random_string(i)
                new_habit.clear()
                new_habit.send_keys(habit)
                time.sleep(1)  # cause error if not wait
                create.click()
                ct = ct+1
                xp = "zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xp))
                    )
                except TimeoutException:
                    assert True, ("load slowly")

                finally:
                    assert habit == driver.find_element_by_xpath(
                        "//zg-body/zg-row[last()]/"
                        "zg-cell[2]").text, "Wrong Habit Name"

            # log_button
            log_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']")
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']/div")
            sl = []
            for streak in streak_list:
                sl.append(int(''.join(filter(str.isdigit, streak.text))))
            # driver.find_element_by_xpath("//form[@id='loginForm']")
            for button in log_button:
                # driver.execute_script("document.getElementsByClassName('log-button')[0].click()")
                driver.execute_script("arguments[0].click()", button)
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']")
            for i, j in zip(sl, streak_list):
                # print(type(i))
                # print(int(''.join(filter(str.isdigit, j.text))))
                assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                    ), "wrong streak"

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()


class TestHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome()

    def test_habit(self):
        driver = self.driver
        html_file = os.path.abspath(
            '..') + "/sandbox/grid_demo_habit_manager.html"
        driver.get("file:" + html_file)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "zg-head-cell"))
            )
        except TimeoutException:
            assert True, ("load slowly")
        finally:
            new_habit = driver.find_element_by_xpath(
                "//input[@id ='new-habit']")
            create = driver.find_element_by_xpath("//button[@id ='add']")
            ct = len(driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']"))
            for i in range(1, 10):
                habit = get_random_string(i)
                new_habit.clear()
                new_habit.send_keys(habit)
                time.sleep(1)
                create.click()
                ct = ct+1
                xp = "zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xp))
                    )
                except TimeoutException:
                    assert True, ("load slowly")

                finally:
                    assert habit == driver.find_element_by_xpath(
                        "//zg-body/zg-row[last()]/zg-cell[2]/"
                        "div").text, "Wrong Habit Name"

            # log_button
            log_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']")
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']/div")
            sl = []
            for streak in streak_list:
                sl.append(int(''.join(filter(str.isdigit, streak.text))))
            # driver.find_element_by_xpath("//form[@id='loginForm']")
            for button in log_button:
                # driver.execute_script("document.getElementsByClassName('log-button')[0].click()")
                driver.execute_script("arguments[0].click()", button)
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']")
            for i, j in zip(sl, streak_list):
                # print(type(i))
                # print(int(''.join(filter(str.isdigit, j.text))))
                assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                    ), "wrong streak"

            # delete button
            remove_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@action = 'removerecord']")
            length = len(remove_button)
            tmp = length
            delete = driver.execute_script(
                'return document.querySelector("zg-dialog").shadowRoot.'
                'querySelector("button.zg-dialog-confirm")')
            if delete is None:
                print("null")

            for button in remove_button:
                driver.execute_script("arguments[0].click()", button)
                # time.sleep(5)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//zg-dialog[@open]"))
                    )
                except TimeoutException:
                    assert True, ("load slowly")
                else:
                    delete.click()
                    assert (length-len(driver.find_elements_by_xpath(
                        "(//zing-grid/zg-body/zg-row"
                        "[@hidden])"))) == tmp - 1, "Wrong delete"
                    # time.sleep(5)
                    tmp = tmp - 1

            new_habit = driver.find_element_by_xpath(
                "//input[@id ='new-habit']")
            create = driver.find_element_by_xpath("//button[@id ='add']")
            ct = len(driver.find_elements_by_xpath(
                "//zing-grid/zg-body/zg-row[not(@hidden)]"))
            for i in range(1, 10):
                habit = get_random_string(i)
                new_habit.clear()
                new_habit.send_keys(habit)
                time.sleep(1)
                create.click()
                ct = ct+1
                xp = "zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, xp))
                    )
                except TimeoutException:
                    assert True, ("load slowly")

                finally:
                    assert habit == driver.find_element_by_xpath(
                        "(//zg-body/zg-row[not (@hidden)])[last()]/"
                        "zg-cell[2]").text, "Wrong Habit Name"

            # log_button
            log_button = driver.find_elements_by_xpath(
                "//zg-body//zg-button[@class = 'log-button']")
            streak_list = driver.find_elements_by_xpath(
                "//zg-body//zg-cell[@data-field-index='streak']/div")
            sl = []
            for streak in streak_list:
                sl.append(int(''.join(filter(str.isdigit, streak.text))))
            # driver.find_element_by_xpath("//form[@id='loginForm']")
            for button in log_button:
                # driver.execute_script("document.getElementsByClassName('log-button')[0].click()")
                driver.execute_script("arguments[0].click()", button)
            streak_list = driver.find_elements_by_xpath(
                "//zg-body/zg-row[not (@hidden)]/zg-cell"
                "[@data-field-index='streak']")
            for i, j in zip(sl, streak_list):
                # print(type(i))
                print(int(''.join(filter(str.isdigit, j.text))))
                assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                    ), "wrong streak"

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()
