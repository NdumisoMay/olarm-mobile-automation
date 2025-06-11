import time

from appium.webdriver.common.appiumby import AppiumBy

from helpers.common_tests import first_login_btn, do_login, select_device
from pages.areas_page import AreasPage
from pages.device_setup_page import DeviceSetupPage


def test_navigate_to_device_settings(driver):
    first_login_btn(driver)
    do_login(driver)
    select_device(driver)
    device_setup = DeviceSetupPage(driver)
    device_setup.nav_to_device_setup()
    locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Timezone")')
    element = device_setup.is_visible(locator)
    time.sleep(5)
    assert element is not None, "❌ 'Timezone' screen did not appear."
    actual_text = element.text.strip()
    expected_text = "Timezone"
    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"

