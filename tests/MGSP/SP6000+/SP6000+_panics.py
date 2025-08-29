import time
import pytest

from helpers.common_tests import select_device, first_login_btn, do_login, do_disarm
from pages.areas_page import AreasPage
from pages.zones_page import ZonesPage
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


def test_go_to_panic_screen(session_driver):
    """Test: Panic button in bottom navigation"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = PanicPage(session_driver)
    page.click_panic_button_bottom_nav()
    #assert page.is_element_visible(page.send_panic_title)
    assert page.is_element_visible(page.emergency_type_label)
    assert page.is_element_visible(page.fire_button)
    assert page.is_element_visible(page.panic_button)
    assert page.is_element_visible(page.medical_button)
    assert page.is_element_visible(page.show_all_emergency_contacts_btn)


def test_fire_panic_btn(session_driver):
    """Test: Panic button in bottom navigation"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = PanicPage(session_driver)
    page.click_panic_button_bottom_nav()
    page.click_fire_emergency()
    assert page.is_element_visible(page.fire_panic_acivated)
    page.click_okay_btn_panic_activated()

def test_panic_btn(session_driver):
    """Test: Panic button in bottom navigation"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = PanicPage(session_driver)
    page.click_panic_button_bottom_nav()
    page.click_panic_emergency()
    assert page.is_element_visible(page.panic_acivated)
    page.click_okay_btn_panic_activated()

def test_medical_panic_btn(session_driver):
    """Test: Panic button in bottom navigation"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = PanicPage(session_driver)
    page.click_panic_button_bottom_nav()
    page.click_medical_emergency()
    assert page.is_element_visible(page.medical_panic_acivated)
    page.click_okay_btn_panic_activated()

def test_show_all_emergency_contacts(session_driver):
    """Test: Show all emergency contacts"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")

    page = PanicPage(session_driver)
    page.click_panic_button_bottom_nav()
    page.click_show_all_emergency_contacts()
    assert page.is_element_visible(page.emergency_contacts_title)
    assert page.is_element_visible(page.national_emergency)
    assert page.is_element_visible(page.saps_police)
    assert page.is_element_visible(page.er24_ambulance)
    assert page.is_element_visible(page.national_crimestop)
    page.click_emergency_contacts_back_btn()
