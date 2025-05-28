from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LogOutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    drawer_menu = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("icon-button").instance(1)')
    drawer_menu_my_devices= (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("icon-button")')
    logout_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Logout")')

    def logout_user(self):
        self.click(self.drawer_menu)
        self.click(self.logout_btn)

    def logout_my_devices(self):
        self.click(self.drawer_menu_my_devices)
        self.click(self.logout_btn)

