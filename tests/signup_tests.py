import pytest
from appium.webdriver.common.appiumby import AppiumBy

from pages.sign_up_page import UserSignUpPage
from utils.data_reader import read_cell_no_data


@pytest.mark.usefixtures("driver")

class TestSignUp:

    def test_signup_link(self, driver):
        signup_up = UserSignUpPage(driver)
        signup_up.click_user_sign_up_link()

        expected_text = "Select a country or region"
        actual_text = signup_up.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Select a country or region").instance(1)')
        )

        assert (
                actual_text == expected_text
        ), f"Expected '{expected_text}', but got '{actual_text}'"


    def test_submit_without_selecting_country(self, driver):
        element = UserSignUpPage(driver)
        element.get_started()

        expected_text = "Country is required"
        actual_text = element.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Country is required")')
        )

        assert (
                actual_text == expected_text
        ), f"Expected '{expected_text}', but got '{actual_text}'"

    def test_submit_without_ts_and_cs(self, driver):
        element = UserSignUpPage(driver)
        element.get_started()

        expected_text = "Country is required"
        actual_text = element.get_text(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Country is required")')
        )

        assert (
                actual_text == expected_text
        ), f"Expected '{expected_text}', but got '{actual_text}'"

    def test_submit_empty_phone_no(self,driver):
        cell = UserSignUpPage(driver)
        cell.skip_terms_and_no()

        expected_text = "Phone number is required"
        actual_text = cell.get_text(
            (AppiumBy.XPATH, '//android.widget.TextView[@text="Phone number is required"]')
        )

        assert (
                actual_text == expected_text
        ), f"Expected '{expected_text}', but got '{actual_text}'"

    @pytest.mark.parametrize(
        "phone",
        read_cell_no_data("phone_no_val"),
        ids=lambda no: f"SQLi:{no['phone']}"
    )
    def test_combination_of_invalid_cell_nos(self, driver, phone):  # ✅ Add self
        reg = UserSignUpPage(driver)
        reg.signup(phone["phone"])
        assert not reg.is_user_sent_otp(), f"❌ signup worked with: {phone['phone']}"
        assert reg.get_error_message() == "Please check your phone number and try again!"



    def test_reset_app(driver_with_uninstall):
        # This test will uninstall the app after it runs
        ...



