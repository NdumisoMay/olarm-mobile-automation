from appium.webdriver.common.appiumby import AppiumBy

from pages.devices_page import DevicesPage
from pages.login_page import LoginPage
from pages.areas_page import AreasPage
from pages.logout_page import LogOutPage
from utils.data_reader import read_test_data


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
