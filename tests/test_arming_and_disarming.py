import time

import pytest

from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.areas_page import AreasPage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService
from helpers.common_tests import do_login, select_device, do_logout, first_login_btn
from pages.areas_page import AreasPage
from pages.base_page import BasePage

@pytest.mark.usefixtures("driver")
def test_arming(driver):
    first_login_btn(driver)
    do_login(driver)
    select_device(driver)
    areas_page = AreasPage(driver)
    areas_page.arm_panel()
    time.sleep(1)
    info = areas_page.get_area_info_by_label("Front Door")
    assert info["status"] == "Armed"
    assert "Now" in info["time"]


def test_disarming(driver):
   # do_login(driver)
    #select_device(driver)
    areas_page = AreasPage(driver)
    areas_page.disarm_panel()
    time.sleep(15)  # Allow time for UI to reflect state change

    info = areas_page.get_area_info_by_label("Front Door")
    assert info["status"] == "Disarmed"
    assert "Now" in info["time"]
    time.sleep(3)

# def test_logout(driver):
#     do_logout(driver)
#
def test_reset_app(driver_with_uninstall):
    # This test will uninstall the app after it runs
    ...



