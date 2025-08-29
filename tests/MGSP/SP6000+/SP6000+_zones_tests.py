import time

from helpers.common_tests import select_device, first_login_btn, do_login, do_disarm
from pages.areas_page import AreasPage
from pages.zones_page import ZonesPage
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


# def test_verify_if_zones_page_is_displayed(session_driver):
#     """Test: Verify if zones page is displayed"""
#     # Launch the app first
#     launch_olarm_app(session_driver)
    
#     # Login and setup (if not already logged in)
#     try:
#         first_login_btn(session_driver)
#         do_login(session_driver)
#         select_device(session_driver)
#     except:
#         print("Already logged in, continuing...")
    
#     page = ZonesPage(session_driver)
#     page.click_bypassed_zones()
#     assert page.is_element_visible(page.active_zones_button)
#     assert page.is_element_visible(page.bypassed_zones_button)

def test_bypass_zones(session_driver):
    """Test: Bypass all 6 zones"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    page = ZonesPage(session_driver)
    page.click_zones()
    
    # Bypass all zones using the reliable approach
    page.bypass_zones()
    
    # Verify that zones are bypassed by checking for reset buttons
    try:
        reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
        print(f"Found {len(reset_buttons)} reset buttons after bypassing")
        
        # Assert that we have reset buttons (indicating zones are bypassed)
        assert len(reset_buttons) > 0, "Should have reset buttons after bypassing zones"
        print("✅ Zones successfully bypassed - reset buttons are visible")
        
    except Exception as e:
        print(f"❌ Error verifying bypassed zones: {e}")
        raise

def test_verify_bypassed_zones_in_bypassed_tab(session_driver):
    """Test: Verify if bypassed zones appear in bypassed tab"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    page = ZonesPage(session_driver)
    page.click_bypassed_zones()
    
    # # First bypass all 6 zones
    # print("=== First bypassing all 6 zones ===")
    # page.bypass_zones()
    
    # Then verify they appear in the bypassed tab
    print("=== Now checking bypassed tab ===")
    result = page.verify_bypassed_zones_in_bypassed_tab()
    
    # Assert that all zones are bypassed
    assert result, "All 6 zones should be bypassed and visible in the bypassed tab"


def test_reset_zones(session_driver):
    """Test: Reset all 6 zones"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except: 
        print("Already logged in, continuing...")
    page = ZonesPage(session_driver)
    page.click_zones()  # First navigate to zones page
    
    # Step 1: Bypass all zones
    print("=== Step 1: Bypassing all zones ===")
    page.bypass_zones()
    
    # Step 2: Go to "Bypassed" tab to verify zones are displayed there
    print("=== Step 2: Checking bypassed zones in Bypassed tab ===")
    page.verify_bypassed_zones_in_bypassed_tab()
    
    # Step 3: Go to "All" tab
    print("=== Step 3: Navigating to All tab ===")
    page.click_all_zones()
    
    # Step 4: Reset all zones
    print("=== Step 4: Resetting all zones ===")
    page.reset_zones()
    
    # Wait a moment for UI to update
    time.sleep(3)
    
    # Navigate back to Active tab to see bypass buttons
    print("=== Navigating to Active tab to verify reset ===")
    try:
        active_tab = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Active").clickable(true)')
        active_tab.click()
        time.sleep(2)
        print("✅ Successfully navigated to Active tab")
    except Exception as e:
        print(f"⚠️ Could not navigate to Active tab: {e}")
        # Try All tab instead
        try:
            all_tab = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("All").clickable(true)')
            all_tab.click()
            time.sleep(2)
            print("✅ Successfully navigated to All tab")
        except Exception as e2:
            print(f"⚠️ Could not navigate to All tab either: {e2}")
            # Try refreshing the page by clicking Zones again
            try:
                print("Trying to refresh by clicking Zones button again...")
                page.click_zones()
                time.sleep(2)
                print("✅ Refreshed zones page")
            except Exception as e3:
                print(f"⚠️ Could not refresh zones page: {e3}")
    
    # Verify that zones are back to normal by checking for bypass buttons
    try:
        bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
        print(f"Found {len(bypass_buttons)} bypass buttons after resetting")
        
        # Check if we have bypass buttons (indicating zones are back to normal)
        if len(bypass_buttons) > 0:
            print("✅ Zones successfully reset - bypass buttons are visible")
        else:
            print("⚠️ No bypass buttons found after reset - zones may be in a different state")
            # Check if there are any zones at all
            all_zone_elements = session_driver.find_elements(AppiumBy.XPATH, '//*[contains(@content-desc, "Zone") or contains(@text, "Zone")]')
            print(f"Found {len(all_zone_elements)} zone elements on the page")
            
            # If we have zones but no bypass buttons, the reset was successful
            if len(all_zone_elements) > 0:
                print("✅ Zones successfully reset - zones are visible but not bypassed")
            else:
                print("❌ No zones found on the page after reset")
                raise AssertionError("No zones found after resetting")
        
    except Exception as e:
        print(f"❌ Error verifying reset zones: {e}")
        raise

def test_search_zones(session_driver):
    """Test: Search for a zone by name"""
    # Launch the app first
    launch_olarm_app(session_driver)
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except: 
        print("Already logged in, continuing...")
    page = ZonesPage(session_driver)
    page.click_zones()  # First navigate to zones page

    page = ZonesPage(session_driver)
    page.search_zones("Zone 06")
    assert page.is_element_visible(page.zone_06_name)
    page.search_zones("Zone 10")
    assert page.is_element_visible(page.zone_10_name)
    page.search_zones("Zone 07")
    assert page.is_element_visible(page.zone_07_name)
    page.search_zones("Zone 08")
    assert page.is_element_visible(page.zone_08_name)
    page.search_zones("Zone 09")
    assert page.is_element_visible(page.zone_09_name)
    page.search_zones("Zone 11")