from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage

print("BasePage loaded")
class LandingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    login_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")')

    def landing_screen_login_btn(self):
        #print("\n📄 Page source:\n", self.driver.page_source)
        #self.driver.save_screenshot("login_screen.png")
        self.click(self.login_btn)

    def go_to_login(self):
        self.landing_screen_login_btn()


