import random
import string
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException


options = webdriver.ChromeOptions()
# options.add_argument('--headless')


def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script(
        'return arguments[0].shadowRoot', element)
    return shadow_root


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def custom_wait_clickable_and_click(wait, selector, attempts=3):
    count = 0
    while count < attempts:
        try:
            time.sleep(1)
            elem = wait.until(
                EC.element_to_be_clickable(selector)
            )
            elem.click()
            return elem

        except WebDriverException as e:
            # except ElementClickInterceptedException as e:
            if ('is not clickable at point' in str(e)):
                print('Retrying clicking on button.')
                count = count + 1
            else:
                raise e

    raise TimeoutException('custom_wait_clickable timed out')


class TestCreateHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_create(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
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
            ustr = 'testhabit@mail.com'
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

            ustr = 'testhabit@mail.com'
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
                WebDriverWait(driver, 10).until(  # waitforpage
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "zg-head-cell"))
                )
            except TimeoutException:
                assert False, ("load slowly")
            else:
                new_habit = driver.find_element_by_xpath(
                    "//input[@id ='new-habit']")

                ct = len(driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@class = 'log-button']"))
                for i in range(1, 15):
                    habit = get_random_string(i)
                    new_habit.clear()
                    new_habit.send_keys(habit)
                    time.sleep(1)  # cause error if not wait
                    try:
                        wait = WebDriverWait(driver, 10)
                        custom_wait_clickable_and_click(
                            wait, (By.XPATH, "//button[@id ='add']"))
                        # WebDriverWait(driver, 10).until(
                        #     EC.element_to_be_clickable((By.XPATH,
                        #  "//button[@id ='add']"))
                        # )
                    except TimeoutException:
                        assert False, ("button is not clickable")

                    else:
                        # create = driver.find_element_by_xpath(
                        #     "//button[@id ='add']")
                        # create.click()
                        ct = ct+1
                        xp = "//zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, xp))
                            )
                        except TimeoutException:
                            # driver.get_screenshot_as_file("create.png")
                            assert False, ("not create")

                        finally:
                            assert habit == driver.find_element_by_xpath(
                                "//zg-body/zg-row[last()]/"
                                "zg-cell[2]").text, "Wrong Habit Name"

                new_habit.clear()
                new_habit.send_keys(habit)
                time.sleep(1)  # cause error if not wait
                try:
                    wait = WebDriverWait(driver, 10)
                    custom_wait_clickable_and_click(
                        wait, (By.XPATH, "//button[@id ='add']"))
                    #  WebDriverWait(driver, 10).until(
                    #     EC.element_to_be_clickable((By.XPATH,
                    #     "//button[@id ='add']"))
                    # )
                except TimeoutException:
                    assert False, ("button is not clickable")

                else:
                    ct = ct+1
                    xp = "//zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xp))
                        )
                    except TimeoutException:
                        # driver.get_screenshot_as_file("create.png")
                        assert False, ("stuck bc same habit name")

                    finally:
                        assert habit == driver.find_element_by_xpath(
                            "//zg-body/zg-row[last()]/"
                            "zg-cell[2]").text, "Wrong Habit Name"

                # # log_button
                # log_button = driver.find_elements_by_xpath(
                #     "//zg-body//zg-button[@class = 'log-button']")
                # streak_list = driver.find_elements_by_xpath(
                #     "//zg-body//zg-cell[@data-field-index='streak']/div")
                # sl = []
                # for streak in streak_list:
                #     sv = int(''.join(filter(str.isdigit, streak.text)))
                #     sl.append(sv)
                #     assert sv == 0, "new habit streak is not 0"
                # # driver.find_element_by_xpath("//form[@id='loginForm']")
                # for button in log_button:
                #     # driver.execute_script("document.getElementsByClassName(
                #         # 'log-button')[0].click()")
                #     driver.execute_script("arguments[0].click()", button)
                # streak_list = driver.find_elements_by_xpath(
                #     "//zg-body//zg-cell[@data-field-index='streak']")
                # for i, j in zip(sl, streak_list):
                #     # print(type(i))
                #     # print(int(''.join(filter(str.isdigit, j.text))))
                #     assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                #                         ), "wrong streak"

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()


class TestStreak():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_log_button_streak(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
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
            ustr = 'testhabit@mail.com'
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

            ustr = 'testhabit@mail.com'
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
                WebDriverWait(driver, 10).until(  # waitforpage
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "zg-head-cell"))
                )
            except TimeoutException:
                assert False, ("load slowly")
            else:

                log_button = driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@class = 'log-button']")
                streak_list = driver.find_elements_by_xpath(
                    "//zg-body//zg-cell[@data-field-index='streak']/div")
                sl = []
                for streak in streak_list:
                    sv = int(''.join(filter(str.isdigit, streak.text)))
                    sl.append(sv)
                    assert sv == 0, "new habit streak is not 0"

                for button in log_button:
                    # driver.execute_script("document.getElementsByClassName('log-button')[0].click()")
                    driver.execute_script("arguments[0].click()", button)
                    # checkstreaknotdoublecount
                    driver.execute_script("arguments[0].click()", button)

                streak_list = driver.find_elements_by_xpath(
                    "//zg-body//zg-cell[@data-field-index='streak']")

                # assert (len(streak_list) > 0), "not read"
                for i, j in zip(sl, streak_list):
                    # print(type(i))
                    # print(int(''.join(filter(str.isdigit, j.text))))
                    assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                        ), "wrong streak"
                driver.refresh()
                streak_list = driver.find_elements_by_xpath(
                    "//zg-body//zg-cell[@data-field-index='streak']/div")
                for i, j in zip(sl, streak_list):
                    assert (i+1) == int(''.join(filter(str.isdigit, j.text))
                                        ), "wrong streak after refresh"
                print("log-button/streak ok")
                driver.close()
                self.driver = webdriver.Chrome(options=options)
                driver = self.driver
                driver.get("http://127.0.0.1:5000/")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "button"))
                    )
                except TimeoutException:
                    assert False, ("load slowly")
                else:
                    ustr = 'testhabit@mail.com'
                    pstr = 'password123'
                    username = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'signup']//input"
                        "[@name = 'username']")
                    password = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'signup']//input"
                        "[@name = 'password']")
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

                    ustr = 'testhabit@mail.com'
                    pstr = 'password123'
                    username = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'login']//input"
                        "[@name = 'username']")
                    password = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'login']//input"
                        "[@name = 'password']")
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
                        WebDriverWait(driver, 10).until(  # waitforpage
                            EC.presence_of_element_located(
                                (By.TAG_NAME, "zg-head-cell"))
                        )
                    except TimeoutException:
                        assert False, ("load slowly")
                    else:

                        streak_list = driver.find_elements_by_xpath(
                            "//zg-body//zg-cell"
                            "[@data-field-index='streak']/div")
                        for i, j in zip(sl, streak_list):
                            assert (i+1) == int(
                                ''.join(filter(str.isdigit, j.text))
                            ), "wrong streak after reopen"
                        print("log-button/streak ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()


class TestDeleteHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_delete_button(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
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
            ustr = 'testhabit@mail.com'
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

            ustr = 'testhabit@mail.com'
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
                WebDriverWait(driver, 10).until(  # waitforpage
                    EC.presence_of_element_located(
                        (By.TAG_NAME, "zg-head-cell"))
                )
            except TimeoutException:
                assert False, ("load slowly")
            else:
                # log_button = driver.find_elements_by_class_name("log-button")
                remove_button = driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@action = 'removerecord']")
                # assert len(remove_button) > 0, "not read"
                length = len(remove_button)
                tmp = length
                dialog = driver.find_element_by_xpath("//zg-dialog")
                sr = driver.execute_script(
                    'return arguments[0].shadowRoot', dialog)
                # '.querySelector("button.zg-dialog-confirm")'
                delete = sr.find_element_by_css_selector(
                    "button.zg-dialog-confirm")

                for button in remove_button:
                    driver.execute_script("arguments[0].click()", button)

                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//zg-dialog[@open]"))
                        )
                    except TimeoutException:
                        assert False, ("load slowly")
                    else:
                        delete.click()
                        # checkfordeleteonerow
                        remain = driver.find_elements_by_xpath(
                            "//zing-grid/zg-body/zg-row[not(@hidden)]")
                        assert (tmp - 1) == (len(remain)), "Wrong delete"
                        tmp = tmp - 1
                driver.refresh()
                assert (len(driver.find_elements_by_xpath(
                            "//zing-grid/zg-body/zg-row[not(@hidden)]"
                            ))) == tmp, "not delete after refresh"
                driver.close()
                self.driver = webdriver.Chrome(options=options)
                driver = self.driver
                driver.get("http://127.0.0.1:5000/")

                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "button"))
                    )
                except TimeoutException:
                    assert False, ("load slowly")
                else:
                    ustr = 'testhabit@mail.com'
                    pstr = 'password123'
                    username = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'signup']//input"
                        "[@name = 'username']")
                    password = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'signup']//input"
                        "[@name = 'password']")
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

                    ustr = 'testhabit@mail.com'
                    pstr = 'password123'
                    username = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'login']//input"
                        "[@name = 'username']")
                    password = driver.find_elements_by_xpath(
                        "//div/div/div[@id = 'login']//input"
                        "[@name = 'password']")
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
                        WebDriverWait(driver, 10).until(  # waitforpage
                            EC.presence_of_element_located(
                                (By.TAG_NAME, "zg-head-cell"))
                        )
                    except TimeoutException:
                        assert False, ("load slowly")
                    else:
                        assert (len(driver.find_elements_by_xpath(
                            "//zing-grid/zg-body/zg-row[not(@hidden)]"
                        ))) == tmp, "not delete after reopen"

                print("delete habit ok")

    def teardown_method(self, method):
        print("close website")
        time.sleep(3)
        self.driver.close()


class TestLogDelete():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_log_button_streak(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
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
            ustr = 'testhabit@mail.com'
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

            ustr = 'testhabit@mail.com'
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
                assert False, ("load slowly")
            else:
                new_habit = driver.find_element_by_xpath(
                    "//input[@id ='new-habit']")

                ct = len(driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@class = 'log-button']"))
                for i in range(10, 15):
                    habit = get_random_string(i)
                    new_habit.clear()
                    new_habit.send_keys(habit)
                    time.sleep(1)  # cause error if not wait
                    try:
                        wait = WebDriverWait(driver, 10)
                        custom_wait_clickable_and_click(
                            wait, (By.XPATH, "//button[@id ='add']"))
                    except TimeoutException:
                        assert False, ("button is not clickable")

                    else:
                        ct = ct+1
                        xp = "//zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, xp))
                            )
                        except TimeoutException:
                            # driver.get_screenshot_as_file("create.png")
                            assert False, ("not create habit")

                        else:
                            assert habit == driver.find_element_by_xpath(
                                "//zg-body/zg-row[last()]/zg-cell[2]/"
                                "div").text, "Wrong Habit Name"
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
                        assert False, ("load slowly")
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
                        assert (length-len(driver.find_elements_by_xpath(
                            "//zing-grid/zg-body/zg-row"
                            "[@hidden]"))) == tmp - 1, "Wrong delete"
                        # time.sleep(5)
                        tmp = tmp - 1

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()


class TestHabit():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_habit(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            ustr = 'testhabit@mail.com'
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

            ustr = 'testhabit@mail.com'
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
                assert False, ("load slowly")
            else:
                new_habit = driver.find_element_by_xpath(
                    "//input[@id ='new-habit']")

                ct = len(driver.find_elements_by_xpath(
                    "//zg-body//zg-button[@class = 'log-button']"))
                for i in range(10, 15):
                    habit = get_random_string(i)
                    new_habit.clear()
                    new_habit.send_keys(habit)
                    time.sleep(1)  # cause error if not wait
                    try:
                        wait = WebDriverWait(driver, 10)
                        custom_wait_clickable_and_click(
                            wait, (By.XPATH, "//button[@id ='add']"))
                        # WebDriverWait(driver, 10).until(
                        #     EC.element_to_be_clickable((By.XPATH,
                        #     "//button[@id ='add']"))
                        # )
                    except TimeoutException:
                        assert False, ("button is not clickable")

                    else:
                        ct = ct+1
                        xp = "//zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                        try:
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, xp))
                            )
                        except TimeoutException:
                            # driver.get_screenshot_as_file("create.png")
                            assert False, ("not create habit")

                        else:
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
                    time.sleep(1)
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
                        assert False, ("load slowly")
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
                    xp = "//zg-body/zg-row[{}]/zg-cell[2]".format(ct)
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, xp))
                        )
                    except TimeoutException:
                        assert False, ("load slowly")

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
                    time.sleep(1)
                    driver.execute_script("arguments[0].click()", button)

                streak_list = driver.find_elements_by_xpath(
                    "//zg-body/zg-row[not (@hidden)]/zg-cell"
                    "[@data-field-index='streak']")
                for i, j in zip(sl, streak_list):
                    # print(type(i))
                    print(int(''.join(filter(str.isdigit, j.text))))
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
                        assert False, ("load slowly")
                    else:
                        delete.click()
                        assert (length-len(driver.find_elements_by_xpath(
                            "(//zing-grid/zg-body/zg-row"
                            "[@hidden])"))) == tmp - 1, "Wrong delete"
                        # time.sleep(5)
                        streak_list = driver.find_elements_by_xpath(
                            "//zg-body//zg-cell"
                            "[@data-field-index='streak']/div")
                        sl.pop()
                        for i, j in zip(sl, streak_list):
                            # print(type(i))
                            print(int(''.join(filter(str.isdigit, j.text))))
                            assert (i+1) == int(
                                ''.join(filter(str.isdigit, j.text))
                            ), "wrong streak"
                        tmp = tmp - 1

    def teardown_method(self, method):
        driver = self.driver
        remove_button = driver.find_elements_by_xpath(
            "//zg-body//zg-button[@action = 'removerecord']")
        # assert len(remove_button) > 0, "not read"
        length = len(remove_button)
        tmp = length
        dialog = driver.find_element_by_xpath("//zg-dialog")
        sr = driver.execute_script(
            'return arguments[0].shadowRoot', dialog)
        # '.querySelector("button.zg-dialog-confirm")'
        delete = sr.find_element_by_css_selector(
            "button.zg-dialog-confirm")

        for button in remove_button:
            driver.execute_script("arguments[0].click()", button)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//zg-dialog[@open]"))
                )
            except TimeoutException:
                assert False, ("load slowly")
            else:
                delete.click()
                # checkfordeleteonerow
                remain = driver.find_elements_by_xpath(
                    "//zing-grid/zg-body/zg-row[not(@hidden)]")
                assert (tmp - 1) == (len(remain)), "Wrong delete"
                tmp = tmp - 1
        print("close website")
        time.sleep(3)
        # self.driver.close()


class TestWithoutLogIn():

    def setup_method(self, method):
        self.driver = webdriver.Chrome(options=options)

    def test_without_login(self):
        driver = self.driver
        # html_file = os.path.abspath(
        #     '.') + "/sandbox/grid_demo_habit_manager.html"
        # driver.get("file:" + html_file)
        driver.get("http://127.0.0.1:5000/habits")
        # time.sleep(5)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
        except TimeoutException:
            assert False, ("load slowly")
        else:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div/div/div[@id = 'signup']"))
                )
            except TimeoutException:
                assert False, ("not redirect to login page")
            else:
                print("redirect correct")

    def teardown_method(self, method):
        print("close website")
        # time.sleep(3)
        self.driver.close()
