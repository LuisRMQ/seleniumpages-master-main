from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SeleniumWrapper:
    def __init__(self):
        self.driver = webdriver.Edge()

    def open_url(self, url):
        self.driver.get(url)
        time.sleep(5)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    def send_keys(self, element, keys):
        element.send_keys(keys)
        time.sleep(5)

    def click(self, element):
        element.click()
        time.sleep(5)

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def execute_script(self, script, element):
        self.driver.execute_script(script, element)
        time.sleep(2)

    def close_driver(self):
        self.driver.quit()
