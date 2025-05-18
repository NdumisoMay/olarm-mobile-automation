import pytest
from pages.sign_up import UserSignUpPage

@pytest.mark.usefixtures("driver")

class TestSignUp:

    def test_signup_link(self, driver):
        signup_up = UserSignUpPage(driver)
        signup_up.click_user_sign_up_link()