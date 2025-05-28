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
from helpers.common_tests import do_login, select_device, do_logout
from pages.areas_page import AreasPage
from pages.base_page import BasePage

@pytest.mark.usefixtures("driver")
def test_arming(driver):
    do_login(driver)
    select_device(driver)
    areas_page = AreasPage(driver)
    areas_page.arm_panel()
    time.sleep(3)

    info = areas_page.get_area_info_by_label("Front Door")
    assert info["status"] == "Armed"
    assert "Now" in info["time"]

    # # 1. Find the element that uniquely identifies the area
    # area_label_element = areas_page.is_visible(areas_page.area1_label)
    # # 2. Move up to the parent container (usually a ViewGroup)
    # area_container = area_label_element.find_element(AppiumBy.XPATH, "..")
    #
    # # 3. Within this container, find the status and timestamp elements
    # status_element = area_container.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Armed")')
    # timestamp_element = area_container.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" • Now")')
    #
    # # 4. Assertions
    # assert area_label_element.text == "Area 1", "Area label mismatch"
    # assert status_element.text == "Armed", "Area is not armed"
    # assert timestamp_element.text == " • Now", f"Expected timestamp ' • Now', got '{timestamp_element.text}'"


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



