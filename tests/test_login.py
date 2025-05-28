import time

import pytest

from helpers.common_tests import do_logout
from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from pages.logout_page import LogOutPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

@pytest.mark.usefixtures("driver")

class TestLoginFlow:

    def test_click_login_btn(self, driver):
        landing_page = LandingPage(driver)
        landing_page.landing_screen_login_btn()

    def test_invalid_login(self, driver):
        credentials = read_test_data("invalid_user")
        login_page = LoginPage(driver)
        login_page.login(credentials["username"], credentials["password"])
        assert not login_page.is_logged_in(), f"❌ User logged in with: {credentials['username']}"
        assert login_page.get_error_message() == "Please check your credentials and try again!"

    def test_valid_login(self, driver):
        credentials = read_test_data("valid_user")
        login_page = LoginPage(driver)
        login_page.login(credentials["username"], credentials["password"])

        expected_text = "My Devices"
        actual_text = login_page.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Devices")')
        )

        assert (
                actual_text == expected_text
        ), f"Expected '{expected_text}', but got '{actual_text}'"
        time.sleep(10)

    def test_logout(self,driver):
        do_logout(driver)










