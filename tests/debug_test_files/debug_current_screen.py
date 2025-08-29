import time
from appium.webdriver.common.appiumby import AppiumBy
from helpers.common_tests import first_login_btn, do_login, select_device

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

def test_debug_current_screen(session_driver):
    """Debug test to understand what screen the app is currently on"""
    print("=== Debug: Understanding Current Screen ===")
    
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
    
    # Take a screenshot to see current state
    session_driver.save_screenshot("debug_current_screen.png")
    print("📸 Screenshot saved: debug_current_screen.png")
    
    # Try to find common elements that might be on the screen
    common_elements = [
        ("Zones", 'new UiSelector().description("Zones")'),
        ("Areas", 'new UiSelector().description("Areas")'),
        ("Devices", 'new UiSelector().description("Devices")'),
        ("Settings", 'new UiSelector().description("Settings")'),
        ("Activity", 'new UiSelector().description("Activity")'),
        ("Arm", 'new UiSelector().text("Arm")'),
        ("Disarm", 'new UiSelector().text("Disarm")'),
        ("Stay", 'new UiSelector().text("Stay")'),
        ("Sleep", 'new UiSelector().text("Sleep")'),
        ("Area 1", 'new UiSelector().text("Area 1")'),
        ("Area 2", 'new UiSelector().text("Area 2")'),
    ]
    
    print("🔍 Searching for common elements on current screen:")
    found_elements = []
    
    for element_name, selector in common_elements:
        try:
            element = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
            if element.is_displayed():
                print(f"✅ Found: {element_name}")
                found_elements.append(element_name)
            else:
                print(f"⚠️ Found but not visible: {element_name}")
        except Exception:
            print(f"❌ Not found: {element_name}")
    
    print(f"\n📋 Summary: Found {len(found_elements)} visible elements: {found_elements}")
    
    # Try to find any buttons with "Zones" in the text or description
    print("\n🔍 Searching for any elements containing 'Zones':")
    try:
        zones_elements = session_driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Zones') or contains(@content-desc, 'Zones')]")
        print(f"Found {len(zones_elements)} elements containing 'Zones'")
        for i, element in enumerate(zones_elements):
            try:
                text = element.get_attribute('text')
                content_desc = element.get_attribute('content-desc')
                print(f"  Element {i+1}: text='{text}', content-desc='{content_desc}'")
            except Exception as e:
                print(f"  Element {i+1}: Error getting attributes: {e}")
    except Exception as e:
        print(f"Error searching for Zones elements: {e}")
    
    # Get page source to understand the current screen structure
    print("\n📄 Getting page source...")
    try:
        page_source = session_driver.page_source
        with open("debug_page_source.xml", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("📄 Page source saved: debug_page_source.xml")
    except Exception as e:
        print(f"❌ Error getting page source: {e}")
    
    print("\n✅ Debug test completed")
