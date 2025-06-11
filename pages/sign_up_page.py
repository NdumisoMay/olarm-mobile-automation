from helpers.common_tests import select_device
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class UserSignUpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    signup_link = ((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Sign Up")')
    )

    select_region = ((AppiumBy.ANDROID_UIAUTOMATOR,
                      'new UiSelector().className("android.widget.HorizontalScrollView")'))

    select_country = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.view.ViewGroup").instance(7)')

    get_started_btn = (AppiumBy.XPATH,'//android.widget.Button[@content-desc="Get Started"]')

    terms_btn= (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().className("android.widget.CheckBox")')

    cell = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined")')


    def click_user_sign_up_link(self):
        self.click(self.signup_link)

    def register(self):
        self.click(self.select_region)

    def get_started(self):
        self.click(self.get_started_btn)

    def skip_terms_and_no(self):
        self.click(self.select_region)
        self.click(self.select_country)
        self.click(self.get_started_btn)

    def signup(self, phone):
        self.click(self.select_region)
        self.click(self.signup_link)
        self.click(self.select_country)
        self.type(self.cell, phone)
        self.click(self.terms_btn)
        self.click(self.get_started_btn)


    def is_user_sent_otp(self):
        return self.driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Verify your phone")') != []

    def get_error_message(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Please provide a valid mobile number")').text
        except:
            return ""









