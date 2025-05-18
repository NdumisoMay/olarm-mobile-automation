from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class AddDevicePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
#Locate elements

    add_device_btn = (AppiumBy.ACCESSIBILITY_ID, "Add Olarm Device")
    def click_add_device(self):
        self.click(self.add_device_btn)

    click_serial_btn = (AppiumBy.ACCESSIBILITY_ID, "Enter serial")
    def click_serial_button(self):
        self.click(self.click_serial_btn)

    enter_serial_no = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined")')
    enter_verification_code = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="text-input-outlined"]')
    submit_device_details = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    def type_device_details(self, serial, verification_code):
        self.type(self.enter_serial_no,serial)
        self.type(self.enter_verification_code, verification_code)
        self.click(self.submit_device_details)

    device_name = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="text-input-outlined"]')
    next_btn = (AppiumBy.ACCESSIBILITY_ID, "Next")

    def name_device(self,name_of_device):
        self.type(self.device_name,name_of_device)
        self.click(self.next_btn)
