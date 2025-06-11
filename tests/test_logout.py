import pytest
from appium.webdriver.common.appiumby import AppiumBy

from helpers.common_tests import do_login, first_login_btn
from pages.logout_page import LogOutPage

@pytest.mark.usefixtures("driver")

def test_logout(driver):
    first_login_btn(driver)
    do_login(driver)
    logout_page = LogOutPage(driver)
    logout_page.logout_my_devices()

    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")

# def test_reset_app(driver_with_uninstall):
#     # This test will uninstall the app after it runs
#     ...


