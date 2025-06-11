import time

from appium.webdriver.common.appiumby import AppiumBy

from pages.add_device_page import AddDevicePage
from pages.devices_page import DevicesPage
from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.areas_page import AreasPage
from pages.logout_page import LogOutPage
from utils.data_reader import read_test_data, read_device_details


def first_login_btn(driver):
    landing_page = LandingPage(driver)
    landing_page.landing_screen_login_btn()
    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")


def do_login(driver):
    credentials = read_test_data("valid_user")
    login_page = LoginPage(driver)
    login_page.login(credentials["username"], credentials["password"])

def select_device(driver):
    device_list = DevicesPage(driver)
    device_list.select_device()

#logout
def do_logout(driver):
    log_out = LogOutPage(driver)
    log_out.logout_user()
    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")

def do_logout_my_devices(driver):
    log_out = LogOutPage(driver)
    log_out.logout_my_devices()
    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")

#Add device flow common tests

def do_add_olarm_device_btn(driver):
    first_login_btn(driver)
    do_login(driver)
    add_device_btn = AddDevicePage(driver)
    # Scroll to the element by its content-description before clicking it
    add_device_btn.scroll_to_description("Add Olarm Device")
    #time.sleep(1.5)
    add_device_btn.click_add_device()

    # new UiSelector().text("Scan the QR code on the back of your Olarm device.")


def do_click_serial_btn(driver):
    click_serial_btn = AddDevicePage(driver)
    click_serial_btn.click_serial_button()


def do_capture_device_details(driver):
    valid_device_details = read_device_details("valid_device")
    add_device = AddDevicePage(driver)
    add_device.type_device_details(valid_device_details["serial"], valid_device_details["verification_code"])


def do_add_device_name(driver):
    valid_device_name = read_device_details("name_device")
    add_device_name = AddDevicePage(driver)
    add_device_name.name_device(valid_device_name["name_of_device"])

def do_disarm(driver):
   # do_login(driver)
    #select_device(driver)
    areas_page = AreasPage(driver)
    areas_page.disarm_panel()
    time.sleep(15)  # Allow time for UI to reflect state change
