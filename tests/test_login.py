import pytest

from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.login import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

@pytest.mark.usefixtures("driver")
class TestLoginFlow:

    def test_click_login_btn(self, driver):
        landing_page = LandingPage(driver)
        landing_page.landing_screen_login_btn()

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

    def test_add_device(self, driver):
        add_device_btn = AddDevicePage(driver)
        #Scroll to the element by its content-description before clicking it
        add_device_btn.scroll_to_description("Add Olarm Device")
        import time
        time.sleep(1.5)
        add_device_btn.click_add_device()

    def test_click_serial_btn(self, driver):
        click_serial_btn = AddDevicePage(driver)
        click_serial_btn.click_serial_button()

    def test_capture_device_details(self, driver):
        valid_device_details = read_device_details("valid_device")
        add_device = AddDevicePage(driver)
        add_device.type_device_details(valid_device_details["serial"], valid_device_details["verification_code"])

    def test_add_device_name(self, driver):
        valid_device_name = read_device_details("name_device")
        add_device_name = AddDevicePage(driver)
        add_device_name.name_device(valid_device_name["name_of_device"])






