from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class UserSignUpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    signup_link = ((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" Sign Up")')
    )

    select_region = ((AppiumBy.ANDROID_UIAUTOMATOR,
                      'new UiSelector().className("android.widget.HorizontalScrollView")'))

    def click_user_sign_up_link(self):
        self.click(self.signup_link)

    def register(self):
        self.click(self.select_region)


