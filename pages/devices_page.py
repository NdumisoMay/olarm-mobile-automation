from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class DevicesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    select_device_locator = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("1, 2, 3, 4, 5, 6, 7, 8, QA_SP6000+, Ready")')

    def select_device(self):
        self.click(self.select_device_locator)
