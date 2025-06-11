import os
import time
from socket import send_fds

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class AddDevicePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    add_device_btn = (AppiumBy.ACCESSIBILITY_ID, "Add Olarm Device")
    def click_add_device(self):
        self.click(self.add_device_btn)

    click_serial_btn = (AppiumBy.ACCESSIBILITY_ID, "Enter serial")
    def click_serial_button(self):
        self.click(self.click_serial_btn)

    enter_serial_no = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Serial")')
    enter_verification_code = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("vCode")')
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

    secure_sys_opt_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.ViewGroup").instance(23)')
    continue_btn = (AppiumBy.ACCESSIBILITY_ID, 'Continue')

    def connect_to_security_sys(self):
        self.click(self.secure_sys_opt_1)
        self.click(self.continue_btn)

    #UDL/Master
    udl_master_1 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otp_input_0")')
    udl_master_2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otp_input_1")')
    udl_master_3 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otp_input_2")')
    udl_master_4 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("otp_input_3")')
    continue_btn2 = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Continue")')

    def add_udl_master(self, value1, value2, value3, value4):
        self.type(self.udl_master_1, value1)
        self.type(self.udl_master_2, value2)
        self.type(self.udl_master_3, value3)
        self.type(self.udl_master_4, value4)
        #self.driver.save_screenshot("before_continue_click.png")
        time.sleep(2)
        self.click(self.continue_btn2)
        # ✅ Ensure input is finalized before clicking
        try:
            self.driver.hide_keyboard()  # Closes any open keyboard
            time.sleep(1)  # Give the UI time to respond
        except Exception as e:
            print(f"[!] Could not hide keyboard: {e}")

        # ✅ Optional (if keyboard is stubborn or no change):
        try:
            self.driver.press_keycode(66)  # Press Enter/Done key
            time.sleep(1)
        except Exception as e:
            print(f"[!] Could not send keycode: {e}")

        # ✅ Optional: tap outside to blur input field
        try:
            self.driver.execute_script("mobile: clickGesture", {"x": 10, "y": 10})
            time.sleep(1)
        except Exception as e:
            print(f"[!] Tap outside failed: {e}")

        # ✅ Now click Continue
        print("Clicking on:", self.continue_btn)
        self.click(self.continue_btn)

    def is_on_next_screen(self):
        # Example: check that a title or next element appears
        try:
            return WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("This device is only compatible with 2.4GHz Wi-Fi networks.")'))
            )
        except TimeoutException:
            self.driver.save_screenshot("next_screen_not_found.png")
            return False

    #skip steps
    skip_step_master_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Skip this step")')
    skip_step_wifi_btn = (AppiumBy.XPATH,'new UiSelector().resourceId("button")')

    def skip_udl_master(self):
        self.click(self.skip_step_master_btn)

    def skip_wifi(self):
        self.click(self.skip_step_wifi_btn)

    #device setup button
    device_setup_btn = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().description("Device setup")')

    def add_device_device_setup(self):
        self.click(self.device_setup_btn)

    click_wifi = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Olarm")')
    wifi_pass = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("text-input-outlined")')
    connect_wifi_btn = (AppiumBy.ACCESSIBILITY_ID,'Connect to network')
    wifi_con_success = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Connected to Olarm")')


    def wifi_conn(self, password):
        self.click(self.click_wifi)
        self.type(self.wifi_pass, password)


    def click_wifi_connect_btn(self):
        self.click(self.connect_wifi_btn)

    def is_connect_to_network_btn_visible(self):
        return self.is_visible(self.connect_wifi_btn)

    # def is_wifi_connected(self, timeout=20):
    #     return self.is_visible(self.wifi_con_success)

    def get_error_message(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            'new UiSelector().text("Try again")').text
        except:
            return ""

    def is_wifi_connected(self):
        """Check if the Connect to network button is visible."""
        try:
            WebDriverWait(self.driver, 47).until(
                EC.presence_of_element_located(self.wifi_con_success)
            )
            return True
        except TimeoutException:
            self.driver.save_screenshot("wifi_not_connected.png")
            return False

    def get_error_message_existing_device(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Permission Denied. Device already belongs to someone else.")').text
        except:
            return ""

    def is_name_your_device_page_loaded(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Name your Olarm device.")').text
        except:
            return ""

    def is_your_device_added(self, timeout=10):
        locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Device Added Successfully.")')
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.text
        except Exception as e:
            screenshot_path = os.path.join(os.getcwd(), "device_added_fail.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"[❌] 'Device Added Successfully.' not found. Screenshot saved at: {screenshot_path}")
            print(f"[⚠️] Exception: {e}")
            print(f"[📄] Page source:\n{self.driver.page_source}")
            return ""



