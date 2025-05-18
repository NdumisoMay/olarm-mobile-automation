from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
#Locate elements
    username_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined").instance(0)')
    password_input = (AppiumBy.XPATH, '((//android.widget.EditText[@resource-id="text-input-outlined"])[2])')
    login_button = (AppiumBy.ACCESSIBILITY_ID, "Login")

    def login(self, username, password):
        self.type(self.username_input, username)
        self.type(self.password_input, password)
        self.click(self.login_button)