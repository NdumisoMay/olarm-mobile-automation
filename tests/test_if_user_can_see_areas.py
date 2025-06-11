
import pytest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from helpers.common_tests import do_logout_my_devices, do_login, do_logout, first_login_btn
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
    first_login_btn(driver)
    do_login(driver)
    click_device = DevicesPage(driver)
    click_device.select_device()

    # Assert that the label is either "Primary user" or "Secondary user"
    element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("user")')
        )
    )

    user_text = element.text.strip().lower()
    assert user_text in ["primary user", "secondary user"], f"Unexpected user label: {user_text}"

def test_logout(driver):
    do_logout(driver)

def test_reset_app(driver_with_uninstall):
    # This test will uninstall the app after it runs
    ...