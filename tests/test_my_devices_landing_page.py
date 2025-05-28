
import pytest
from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.areas_page import AreasPage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService
from pages.devices_page import DevicesPage

@pytest.mark.usefixtures("driver")
def test_select_device(driver):
    click_device = DevicesPage(driver)
    click_device.select_device_on_my_devices()