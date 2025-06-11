from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LogOutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # More specific locators
    drawer_menu = (AppiumBy.XPATH,'(//android.widget.Button[@resource-id="icon-button"])[2]')
    drawer_menu_my_devices = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("icon-button")')
    logout_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Logout")')
    login_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")')


    def logout_user(self):
        """Perform logout and verify the action"""
        # Wait for and click the drawer menu
        self.wait_and_click(self.drawer_menu)
        
        # Wait for and click logout
        self.wait_and_click(self.logout_btn)
        
        # Verify we're logged out by checking for login button
        return self.is_visible(self.login_button)

    def logout_my_devices(self):
        """Perform logout from my devices and verify the action"""
        # Wait for and click the my devices menu
        self.wait_and_click(self.drawer_menu_my_devices)
        
        # Wait for and click logout
        self.wait_and_click(self.logout_btn)
        
        # Verify we're logged out
        return self.is_visible(self.login_button)

    def is_logged_out(self):
        """Verify if user is logged out by checking for login button"""
        return self.is_visible(self.login_button, timeout=5)

