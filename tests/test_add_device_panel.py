import time

import pytest

from helpers.common_tests import do_login, first_login_btn
from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

class TestAddDevicePanel:

    def test_add_device(self, driver):
        first_login_btn(driver)
        #print(driver.page_source)
        do_login(driver)
        add_device_btn = AddDevicePage(driver)
        # Scroll to the element by its content-description before clicking it
        add_device_btn.scroll_to_description("Add Olarm Device")
        #time.sleep(1.5)
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


    def test_connect_security_system(self, driver):
        connect_sys = AddDevicePage(driver)
        connect_sys.connect_to_security_sys()

    # UDL
    def test_enter_udl_master(self, driver):
        data = read_device_details("UDL_master_data")
        page = AddDevicePage(driver)

        page.add_udl_master(
            str(data["input_1"]),
            str(data["input_2"]),
            str(data["input_3"]),
            str(data["input_4"])
        )
        # call on the instance
        assert page.is_on_next_screen(), "Continue button click did not navigate"


    def test_wifi_conn(self, driver):
        data = read_device_details("Wifi_creds")
        page = AddDevicePage(driver)
        time.sleep(10)
        page.wifi_conn(data["PWD"])
        assert page.is_connect_to_network_btn_visible(), "❌ Connect to network button is not visible"
        print("✅ Connect to network button is not visible")


    def test_connect_to_wifi(self, driver):
        page = AddDevicePage(driver)
        page.click_wifi_connect_btn()
        assert page.is_wifi_connected(), "Connected to network successfully"
        assert not page.get_error_message(),"Wifi connection failed"

    # def test_reset_app(self,driver_with_uninstall):
    #     # This test will uninstall the app after it runs
    #     ...



