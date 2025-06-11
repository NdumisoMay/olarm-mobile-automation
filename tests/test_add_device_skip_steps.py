import time

import pytest

from helpers.common_tests import first_login_btn, do_add_device_name
from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

class TestAddDevicePanel:

    def test_valid_login(self, driver):
        first_login_btn(driver)
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
        # Scroll to the element by its content-description before clicking it
        add_device_btn.scroll_to_description("Add Olarm Device")
        time.sleep(1.5)
        add_device_btn.click_add_device()


    def test_click_serial_btn(self, driver):
        click_serial_btn = AddDevicePage(driver)
        click_serial_btn.click_serial_button()


    def test_capture_device_details(self, driver):
        valid_device_details = read_device_details("valid_device")
        add_device = AddDevicePage(driver)
        add_device.type_device_details(valid_device_details["serial"], valid_device_details["verification_code"])
        time.sleep(2)
        assert add_device.is_name_your_device_page_loaded() == "Name your Olarm device."

    def test_add_device_name(self,driver):
        do_add_device_name(driver)
        name_device = AddDevicePage(driver)
        assert name_device.is_your_device_added() == "Device Added Successfully."

    def test_connect_security_system(self, driver):
        connect_sys = AddDevicePage(driver)
        connect_sys.connect_to_security_sys()

        expected_txt = "Enter your UDL Code"
        actual_text = connect_sys.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Enter your UDL Code")')
        )

        assert (
                actual_text == expected_txt
        ), f"Expected '{expected_txt}', but got '{actual_text}'"


    def test_skip_udl_master(self, driver):
        skip_udl = AddDevicePage(driver)
        skip_udl.skip_udl_master()
        expected_txt = "Connect your Olarm device to your Wi-Fi network for improved speed and reliability."

        actual_text = skip_udl.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Connect your Olarm device to your Wi-Fi network for improved speed and reliability.")')
        )

        assert (
                actual_text == expected_txt
        ), f"Expected '{expected_txt}', but got '{actual_text}'"


    def test_skip_wifi_page(self, driver):
        skip_wi = AddDevicePage(driver)
        # Scroll to the element by its content-description before clicking it
        skip_wi.scroll_to_description("Skip this step")
        time.sleep(1.5)
        skip_wi.skip_wifi()
        expected_txt = "Area 1"

        actual_text = skip_wi.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().text("Area 1")')
        )

        assert (
                actual_text == expected_txt
        ), f"Expected '{expected_txt}', but got '{actual_text}'"

    # def test_reset_app(self,driver_with_uninstall):
    #     # This test will uninstall the app after it runs
    #     ...