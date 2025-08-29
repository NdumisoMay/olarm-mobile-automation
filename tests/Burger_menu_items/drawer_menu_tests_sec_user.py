import time
import pytest

from helpers.common_tests import select_device, first_login_btn, do_login, do_disarm
from pages.areas_page import AreasPage
from pages.zones_page import ZonesPage
from pages.burger_menu_page import BurgerMenuPage
from pages.panic import PanicPage
from appium.webdriver.common.appiumby import AppiumBy

def launch_olarm_app(driver):
    """Launch the Olarm app from the home screen"""
    try:
        # First, try to launch the app directly using the app package
        print("🚀 Attempting to launch Olarm app directly...")
        driver.activate_app("com.olarm.olarm1")
        time.sleep(5)  # Wait for app to launch
        print("✅ Olarm app launched successfully using app package")
        return True
    except Exception as e:
        print(f"❌ Failed to launch app directly: {e}")
        
        # Fallback: try to find and click the Olarm app icon
        try:
            print("🔍 Looking for Olarm app icon on home screen...")
            
            # Try different ways to find the Olarm app
            olarm_selectors = [
                (AppiumBy.XPATH, "//android.widget.TextView[@text='Olarm']"),
                (AppiumBy.XPATH, "//*[@content-desc='Olarm']"),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Olarm")'),
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Olarm")'),
            ]
            
            for selector_type, selector_value in olarm_selectors:
                try:
                    olarm_icon = driver.find_element(selector_type, selector_value)
                    if olarm_icon.is_displayed():
                        print(f"✅ Found Olarm app icon with selector: {selector_type}, {selector_value}")
                        olarm_icon.click()
                        time.sleep(5)  # Wait for app to launch
                        print("✅ Olarm app launched successfully")
                        return True
                except Exception:
                    continue
            
            print("❌ Could not find Olarm app icon on home screen")
            return False
            
        except Exception as e2:
            print(f"❌ Error looking for Olarm app icon: {e2}")
            return False


def test_device_status(session_driver):
    """Test: Click on the device status"""
    # Launch the app first
    launch_olarm_app(session_driver)
    page = BurgerMenuPage(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
        # Open the drawer menu after login
        page.click_drawer_menu()
    except:
        print("Already logged in, continuing...")
        # Open the drawer menu even if already logged in
        page.click_drawer_menu()
    
    page.click_device_status()
    assert page.is_element_visible(page.panel_ac_power)
    assert page.is_element_visible(page.panel_ac_power_value)
    assert page.is_element_visible(page.panel_battery_power)
    assert page.is_element_visible(page.panel_battery_power_value)
    assert page.is_element_visible(page.power_input)
    assert page.is_element_visible(page.power_input_value)
    assert page.is_element_visible(page.backup_power)
    assert page.is_element_visible(page.backup_power_value)
    assert page.is_element_visible(page.antenna)
    assert page.is_element_visible(page.antenna_value)
    assert page.is_element_visible(page.cellular_signal_strength)
    assert page.is_element_visible(page.cellular_signal_strength_value)
    page.click_back_status_page()

        
def test_view_profile(session_driver):
    """Test: Click on the view profile"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = BurgerMenuPage(session_driver)
    page.click_drawer_menu()
    page.click_view_profile()
    assert page.is_element_visible(page.profile_title)
    assert page.is_element_visible(page.account_setup_text)
    page.click_account_setup_back_btn()

def test_cant_get_notifications(session_driver):
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = BurgerMenuPage(session_driver)
    page.click_drawer_menu()
    page.click_device_notifications()
    assert page.is_element_visible(page.device_notifications_title)
    assert page.is_element_visible(page.dn_arm_partial_arm_disarm_notifications)
    assert page.is_element_visible(page.reminder_and_alerts)
    assert page.is_element_visible(page.cant_get_notifications)
    page.click_cant_get_notifications_link()
    assert page.is_element_visible(page.cant_get_notifications_notification_and_alerts_page)
    page.click_notification_and_alerts_close_btn()
    # Close the Device Notifications modal
    page.dismiss_device_notifications_modal()

def test_disable_arm_partial_arm_disarm_notifications(session_driver):
    """Test: Disable arm, partial arm and disarm notifications"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = BurgerMenuPage(session_driver)
    page.click_drawer_menu()
    page.click_device_notifications()
    page.click_toggle_to_disable_arm_partial_arm_disarm_notifications()
    assert page.is_element_visible(page.turn_off_notifications_title)
    assert page.is_element_visible(page.turn_off_notifications_warning_msg)
    assert page.is_element_visible(page.turn_off_notifications_confirm_btn)
    assert page.is_element_visible(page.turn_off_notifications_cancel_btn)
    page.click_turn_off_notifications_confirm_btn()
    # Close the Device Notifications modal
    page.dismiss_device_notifications_modal()

def test_turn_on_arm_partial_arm_disarm_notifications(session_driver):
    """Test: Turn on arm, partial arm and disarm notifications"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = BurgerMenuPage(session_driver)
    page.click_drawer_menu()
    page.click_device_notifications()
    page.click_toggle_to_enable_arm_partial_arm_disarm_notifications()
    try:
        page.click_turn_off_notifications_confirm_btn()
    except:
        print("Confirm button not found, continuing...")
    page.dismiss_device_notifications_modal()
   

def test_terms_of_service(session_driver):
    """Test: Click on the terms of service and navigate back"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = BurgerMenuPage(session_driver)
    page.click_drawer_menu()
    page.click_terms_of_service()
    
    # Verify Terms of Service page elements are visible
    assert page.is_element_visible(page.terms_of_service_page_title)
    assert page.is_element_visible(page.terms_of_service_instruction)
    assert page.is_element_visible(page.terms_of_service_body)
    
    # Navigate back to the app
    page.navigate_back_from_terms_of_service()
    
    # Verify we're back in the app (you might want to check for a specific element)
    time.sleep(2)  # Give time for navigation
    print("✅ Successfully completed Terms of Service test")