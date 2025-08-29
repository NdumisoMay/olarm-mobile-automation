import time
from appium.webdriver.common.appiumby import AppiumBy
from helpers.common_tests import first_login_btn, do_login, select_device

def launch_olarm_app(driver):
    """Launch the Olarm app from the home screen"""
    try:
        print("🚀 Attempting to launch Olarm app directly...")
        driver.activate_app("com.olarm.olarm1")
        time.sleep(5)
        print("✅ Olarm app launched successfully using app package")
        return True
    except Exception as e:
        print(f"❌ Failed to launch app directly: {e}")
        return False

def test_debug_reset_verification(session_driver):
    """Debug test to understand what happens after resetting zones"""
    print("=== Debug: Understanding Reset Verification ===")
    
    # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
        print("✅ Login and device selection completed")
    except Exception as e:
        print(f"⚠️ Login/device selection issue: {e}")
    
    # Click on Zones button
    try:
        zones_button = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Zones")')
        zones_button.click()
        time.sleep(3)
        print("✅ Zones button clicked successfully")
    except Exception as e:
        print(f"❌ Error clicking zones button: {e}")
        return
    
    # Take a screenshot before any operations
    session_driver.save_screenshot("debug_before_operations.png")
    print("📸 Screenshot saved: debug_before_operations.png")
    
    # Check initial state
    print("\n🔍 Initial state check:")
    try:
        bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
        reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
        print(f"Initial bypass buttons: {len(bypass_buttons)}")
        print(f"Initial reset buttons: {len(reset_buttons)}")
    except Exception as e:
        print(f"Error checking initial state: {e}")
    
    # Try to bypass some zones first
    print("\n🔄 Attempting to bypass zones:")
    try:
        bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
        print(f"Found {len(bypass_buttons)} bypass buttons to click")
        
        for i, button in enumerate(bypass_buttons[:3]):  # Bypass first 3 zones
            try:
                button.click()
                time.sleep(1)
                print(f"✅ Bypassed zone {i+1}")
            except Exception as e:
                print(f"❌ Error bypassing zone {i+1}: {e}")
    except Exception as e:
        print(f"Error during bypass: {e}")
    
    # Take screenshot after bypassing
    session_driver.save_screenshot("debug_after_bypass.png")
    print("📸 Screenshot saved: debug_after_bypass.png")
    
    # Check state after bypassing
    print("\n🔍 State after bypassing:")
    try:
        bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
        reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
        print(f"Bypass buttons after bypassing: {len(bypass_buttons)}")
        print(f"Reset buttons after bypassing: {len(reset_buttons)}")
    except Exception as e:
        print(f"Error checking state after bypass: {e}")
    
    # Try to reset zones
    print("\n🔄 Attempting to reset zones:")
    try:
        reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
        print(f"Found {len(reset_buttons)} reset buttons to click")
        
        for i, button in enumerate(reset_buttons):
            try:
                button.click()
                time.sleep(2)
                print(f"✅ Reset zone {i+1}")
                
                # Refresh the list to avoid stale elements
                reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
            except Exception as e:
                print(f"❌ Error resetting zone {i+1}: {e}")
                break
    except Exception as e:
        print(f"Error during reset: {e}")
    
    # Take screenshot after resetting
    session_driver.save_screenshot("debug_after_reset.png")
    print("📸 Screenshot saved: debug_after_reset.png")
    
    # Check state after resetting
    print("\n🔍 State after resetting:")
    try:
        bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
        reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
        print(f"Bypass buttons after resetting: {len(bypass_buttons)}")
        print(f"Reset buttons after resetting: {len(reset_buttons)}")
    except Exception as e:
        print(f"Error checking state after reset: {e}")
    
    # Try different tabs
    print("\n🔍 Checking different tabs:")
    tabs_to_check = ["All", "Active", "Bypassed"]
    
    for tab_name in tabs_to_check:
        try:
            print(f"\n--- Checking {tab_name} tab ---")
            tab_element = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().description("{tab_name}").clickable(true)')
            tab_element.click()
            time.sleep(2)
            
            # Check buttons on this tab
            bypass_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
            reset_buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
            print(f"  Bypass buttons on {tab_name} tab: {len(bypass_buttons)}")
            print(f"  Reset buttons on {tab_name} tab: {len(reset_buttons)}")
            
            # Take screenshot of this tab
            session_driver.save_screenshot(f"debug_{tab_name.lower()}_tab.png")
            print(f"  📸 Screenshot saved: debug_{tab_name.lower()}_tab.png")
            
        except Exception as e:
            print(f"  ❌ Error checking {tab_name} tab: {e}")
    
    # Get page source to understand the current state
    print("\n📄 Getting page source...")
    try:
        page_source = session_driver.page_source
        with open("debug_reset_verification_source.xml", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("📄 Page source saved: debug_reset_verification_source.xml")
    except Exception as e:
        print(f"❌ Error getting page source: {e}")
    
    print("\n✅ Debug test completed")

