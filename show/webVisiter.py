from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions


class webVisiter:

    def __init__(self, allow):
        __option = Options()
        __option.add_argument('disable-blink-features=AutomationControlled')
        if not allow:
            __option.add_argument('headless')
        self.browser = Chrome(options=__option)

    def setTimeOut(self, sec):
        self.browser.set_page_load_timeout(sec)

    def load(self, url):
        try:
            self.browser.get(url)
        except:
            self.load(url)

    def isElementFromClass(self, value):
        try:
            self.browser.find_elements_by_class_name(value)
            return True
        except exceptions.NoSuchElementException:
            return False

    def isElementFromID(self, value):
        try:
            self.browser.find_element_by_id(value)
            return True
        except exceptions.NoSuchElementException:
            return False

    def isElementFromTag(self, value):
        try:
            self.browser.find_elements_by_tag_name(value)
            return True
        except exceptions.NoSuchElementException:
            return False
