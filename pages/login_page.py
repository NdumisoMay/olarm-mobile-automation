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

    def is_logged_in(self):
        return self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Devices")') != []

    def get_error_message(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Please check your credentials and try again!")').text
        except:
            return ""