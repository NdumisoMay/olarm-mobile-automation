# import time
#
# import pytest
#
# from helpers.common_tests import do_logout, do_logout_my_devices, first_login_btn
# from pages import add_device_page
# from pages.add_device_page import AddDevicePage
# from pages.base_page import BasePage
# from pages.login_page import LoginPage
# from pages.landing_page import LandingPage
# from pages.logout_page import LogOutPage
# from utils.data_reader import read_test_data, read_device_details
# from appium.webdriver.common.appiumby import AppiumBy
# from appium.webdriver.appium_service import AppiumService
# from pytest_bdd import given, when, then, scenarios
#
# scenarios('../features/login.feature')
# @pytest.mark.usefixtures("driver")
#
# #class TestLoginFlow:
#
# @given("the user is on the landing screen")
# def step_on_landing_screen(driver):
#     first_login_btn(driver)
#
#
# @given("the user is on the login screen")
# def step_on_login_screen(driver):
#     first_login_btn(driver)
#
#
# @when("the user clicks the login button")
# def step_click_login_button(driver):
#     landing_page = LandingPage(driver)
#     landing_page.landing_screen_login_btn()
#
#
# @when("the user enters invalid credentials")
# def step_invalid_login(driver):
#     creds = read_test_data("invalid_user")
#     LoginPage(driver).login(creds["username"], creds["password"])
#
#
# @when("the user enters valid credentials")
# def step_valid_login(driver):
#     creds = read_test_data("valid_user")
#     LoginPage(driver).login(creds["username"], creds["password"])
#
#
# @then("the username and password fields should be visible")
# def step_check_login_fields(driver):
#     page = LoginPage(driver)
#     assert page.is_username_visible(), "❌ Username field not visible"
#     assert page.is_password_visible(), "❌ Password field not visible"
#
#
# @then("an error message should be displayed")
# def step_check_error_message(driver):
#     page = LoginPage(driver)
#     assert page.get_error_message() == "Please check your credentials and try again!"
#
#
# @then("the user should be logged in successfully")
# def step_check_successful_login(driver):
#     actual = LoginPage(driver).get_text(
#         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Devices")')
#     )
#     assert actual == "My Devices", "Failed to verify successful login"
#
#
# @given("the user is logged in")
# def step_user_is_logged_in(driver):
#     first_login_btn(driver)
#     creds = read_test_data("valid_user")
#     LoginPage(driver).login(creds["username"], creds["password"])
#     actual = LoginPage(driver).get_text(
#         (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("My Devices")')
#     )
#     assert actual == "My Devices", "Failed to verify user is logged in"
#
#
# @when("the user performs logout from My Devices")
# def step_perform_logout(driver):
#     do_logout_my_devices(driver)
#
#
# @then("the user should be returned to the login screen")
# def step_verify_returned_to_login(driver):
#     login_page = LoginPage(driver)
#     assert login_page.is_username_visible(), "❌ Username field not visible after logout"
#     assert login_page.is_password_visible(), "❌ Password field not visible after logout"
#
#
# @given("the app is installed")
# def step_app_is_installed(driver):
#     """Verify app is installed by checking if we can access the landing screen"""
#     try:
#         first_login_btn(driver)
#         return True
#     except Exception as e:
#         print(f"❌ Failed to verify app installation: {str(e)}")
#         return False
#
#
# # @when("the app is reset")
# # def step_reset_app(driver_with_uninstall):
# #     """Reset the app by terminating and removing it"""
# #     try:
# #         app_package = device_farm_config["app_package"]
# #         driver_with_uninstall.terminate_app(app_package)
# #         driver_with_uninstall.remove_app(app_package)
# #         return True
# #     except Exception as e:
# #         print(f"❌ Failed to reset app: {str(e)}")
# #         return False
#
#
# @then("the app should be uninstalled successfully")
# def step_verify_app_uninstalled(driver_with_uninstall):
#     """Verify the app is uninstalled by checking it's not installed"""
#     try:
#         app_package = device_farm_config["app_package"]
#         is_installed = driver_with_uninstall.is_app_installed(app_package)
#         assert not is_installed, "App is still installed"
#         return True
#     except Exception as e:
#         print(f"❌ Failed to verify app uninstallation: {str(e)}")
#         return False
#
#
#
#
#
#
#
#
#
