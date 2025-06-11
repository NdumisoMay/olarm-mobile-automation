import time
from socket import send_fds

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class ZonesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
# Locate elements

