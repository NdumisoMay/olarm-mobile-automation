import time
import pytest
from helpers.common_tests import first_login_btn, do_add_olarm_device_btn, do_click_serial_btn, \
    do_capture_device_details, do_add_device_name
from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.device_setup_page import DeviceSetupPage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_test_data, read_device_details
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

def test_ds_test_add_device(driver):
    first_login_btn(driver)
    do_add_olarm_device_btn(driver)
    add_device_btn = AddDevicePage(driver)
    add_device_btn.click_add_device()
    # Checking for the presence of "Scan the QR code on the back of your Olarm device."
    locator = (
    AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Scan the QR code on the back of your Olarm device.")')
    element = add_device_btn.is_visible(locator)

    assert element is not None, "❌ 'Scan the QR code on the back.....' screen did not appear."
    actual_text = element.text.strip()
    expected_text = "Scan the QR code on the back of your Olarm device."
    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"


def test_click_serial_btn(driver):
    do_click_serial_btn(driver)
    serial = AddDevicePage(driver)

    locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("The serial number and verification code can be found on the back of your device")')
    element = serial.is_visible(locator)

    assert element is not None, "❌ 'Serial bottom sheet did not appear' screen did not appear."
    actual_text = element.text.strip()
    expected_text = "The serial number and verification code can be found on the back of your device"
    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"

def test_capture_device_info(driver):
    do_capture_device_details(driver)
    name_device = AddDevicePage(driver)

    locator = (
        AppiumBy.XPATH,
        '//*[@text="Name your Olarm device."]'
    )
    element = name_device.is_visible(locator)

    assert element is not None, "❌ 'Name your Olarm device.' screen did not appear."
    actual_text = element.text.strip()
    expected_text = "Name your Olarm device."
    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"

def test_add_device_name(driver):
    do_add_device_name(driver)
    name_device = AddDevicePage(driver)
    assert name_device.is_your_device_added() == "Device Added Successfully."


def test_navigate_to_device_setup(driver):
    ds_nav = AddDevicePage(driver)
    ds_nav.add_device_device_setup()
    # Checking for the presence of "Timezone"
    locator = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Timezone")')
    element = ds_nav.is_visible(locator)

    assert element is not None, "❌ 'Timezone' screen did not appear."

    actual_text = element.text.strip()
    expected_text = "Timezone"
    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"

def test_factory_reset(driver):
    page = DeviceSetupPage(driver)
    page.scroll_to_description("Remove / Reset Olarm")
    page.perform_factory_reset()
    print("✅ Factory reset and agreement steps completed successfully.")


def test_reset_app(driver_with_uninstall):
    # This test will uninstall the app after it runs
    ...

