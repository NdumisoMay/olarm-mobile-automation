from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
#Locate elements
    username_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined").instance(0)')
    password_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined").instance(1)')
    login_button = (AppiumBy.ACCESSIBILITY_ID, "Login")

    #Old app locators
    username_old_app = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("pageLoginEmail")')
    password_old_app = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("pageLoginPass")')
    sign_in_button_classic_app = (AppiumBy.XPATH, '//android.widget.Button[@text="Sign In"]')
    login_btn_classic = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button")')

#Old app login method
    def old_app_login(self, username, password):
        self.click(self.sign_in_button_classic_app)
        self.type(self.username_old_app, username)
        self.type(self.password_old_app, password)
        self.click(self.login_btn_classic) 


    def login(self, username, password):
        self.type(self.username_input, username)
        self.type(self.password_input, password)
        self.click(self.login_button)

    def is_username_visible(self):
        return self.is_visible(self.username_input)

    def is_password_visible(self):
        return self.is_visible(self.password_input)

    def is_logged_in(self):
        return self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Devices")') != []

    def get_error_message(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Please check your credentials and try again!")').text
        except:
            return ""