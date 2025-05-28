import time

import pytest

from pages import add_device_page
from pages.add_device_page import AddDevicePage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from utils.data_reader import read_sql_injection_data
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.appium_service import AppiumService

@pytest.mark.usefixtures("driver")
@pytest.mark.parametrize(
    "credentials",
    read_sql_injection_data("SQL_injection_tests"),
    ids=lambda cred: f"SQLi:{cred['username']}"
)
def test_sql_injection_login(driver, credentials):
    login_page = LoginPage(driver)
    login_page.login(credentials["username"], credentials["password"])
    assert not login_page.is_logged_in(), f"❌ Injection worked with: {credentials['username']}"
    assert login_page.get_error_message() == "Please check your credentials and try again!"
