import time
from socket import send_fds

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class DeviceSetupPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    
    #Factory reset device
    factory_reset_btn = (AppiumBy.ANDROID_UIAUTOMATOR,
 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Remove / Reset Olarm"))')
    agree_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(49)')

    def perform_factory_reset(self, timeout=10):
        print("➡️ Clicking Factory Reset button")
        self.click(self.factory_reset_btn)

        # Give UI a moment before waiting
        time.sleep(1)

        print("⏳ Waiting for Agree button")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.agree_btn)
            )
        except Exception:
            print("❌ Page source dump:\n", self.driver.page_source)
            self.driver.save_screenshot("agree_button_error.png")
            raise AssertionError("❌ 'Agree' button not visible after clicking 'Factory Reset'")

        assert self.driver.find_element(*self.agree_btn).is_displayed(), "❌ 'Agree' button not displayed"
        print("✅ Clicking Agree")
        self.click(self.agree_btn)

    
    

