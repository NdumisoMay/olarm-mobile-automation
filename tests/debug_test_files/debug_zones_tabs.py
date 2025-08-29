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

def test_debug_zones_tabs(session_driver):
    """Debug test to see what tabs are available on the zones page"""
    print("=== Debug: Checking Zones Page Tabs ===")
    
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
    
    # Take a screenshot to see current state
    session_driver.save_screenshot("debug_zones_page.png")
    print("📸 Screenshot saved: debug_zones_page.png")
    
    # Try to find all possible tab elements
    print("\n🔍 Searching for tab elements on zones page:")
    
    # Common tab selectors
    tab_selectors = [
        ("Zones", 'new UiSelector().description("Zones")'),
        ("Active", 'new UiSelector().description("Active")'),
        ("Bypassed", 'new UiSelector().description("Bypassed")'),
        ("All", 'new UiSelector().description("All")'),
        ("Activity", 'new UiSelector().description("Activity")'),
        ("Areas", 'new UiSelector().description("Areas")'),
        ("Devices", 'new UiSelector().description("Devices")'),
        ("Settings", 'new UiSelector().description("Settings")'),
    ]
    
    found_tabs = []
    
    for tab_name, selector in tab_selectors:
        try:
            element = session_driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
            if element.is_displayed():
                print(f"✅ Found tab: {tab_name}")
                found_tabs.append(tab_name)
                
                # Try to get more details about the element
                try:
                    text = element.get_attribute('text')
                    content_desc = element.get_attribute('content-desc')
                    resource_id = element.get_attribute('resource-id')
                    print(f"   - text: '{text}', content-desc: '{content_desc}', resource-id: '{resource_id}'")
                except Exception as e:
                    print(f"   - Error getting attributes: {e}")
            else:
                print(f"⚠️ Found but not visible: {tab_name}")
        except Exception:
            print(f"❌ Not found: {tab_name}")
    
    print(f"\n📋 Summary: Found {len(found_tabs)} visible tabs: {found_tabs}")
    
    # Try to find any elements containing "Bypassed" text
    print("\n🔍 Searching for any elements containing 'Bypassed':")
    try:
        bypassed_elements = session_driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Bypassed') or contains(@content-desc, 'Bypassed')]")
        print(f"Found {len(bypassed_elements)} elements containing 'Bypassed'")
        for i, element in enumerate(bypassed_elements):
            try:
                text = element.get_attribute('text')
                content_desc = element.get_attribute('content-desc')
                resource_id = element.get_attribute('resource-id')
                print(f"  Element {i+1}: text='{text}', content-desc='{content_desc}', resource-id='{resource_id}'")
            except Exception as e:
                print(f"  Element {i+1}: Error getting attributes: {e}")
    except Exception as e:
        print(f"Error searching for Bypassed elements: {e}")
    
    # Try to find any clickable elements that might be tabs
    print("\n🔍 Searching for clickable elements that might be tabs:")
    try:
        clickable_elements = session_driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
        print(f"Found {len(clickable_elements)} clickable elements")
        
        # Filter for elements that might be tabs (have text or content-desc)
        potential_tabs = []
        for element in clickable_elements:
            try:
                text = element.get_attribute('text')
                content_desc = element.get_attribute('content-desc')
                if text or content_desc:
                    potential_tabs.append((text, content_desc))
            except:
                continue
        
        print(f"Found {len(potential_tabs)} potential tab elements:")
        for text, content_desc in potential_tabs[:10]:  # Limit to first 10
            print(f"  - text: '{text}', content-desc: '{content_desc}'")
            
    except Exception as e:
        print(f"Error searching for clickable elements: {e}")
    
    # Get page source to understand the current screen structure
    print("\n📄 Getting page source...")
    try:
        page_source = session_driver.page_source
        with open("debug_zones_page_source.xml", "w", encoding="utf-8") as f:
            f.write(page_source)
        print("📄 Page source saved: debug_zones_page_source.xml")
    except Exception as e:
        print(f"❌ Error getting page source: {e}")
    
    print("\n✅ Debug test completed")

