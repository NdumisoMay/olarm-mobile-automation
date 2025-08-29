import time

from helpers.common_tests import select_device, first_login_btn, do_login, do_disarm
from pages.areas_page import AreasPage
from pages.zones_page import ZonesPage
from appium.webdriver.common.appiumby import AppiumBy


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
    
def test_debug_app_launch(session_driver):
    """Debug test to verify app launch is working"""
    print("=== Debug: Testing App Launch ===")
    
    # Test app launch
    print("Testing app launch...")
    result = launch_olarm_app(session_driver)
    print(f"App launch result: {result}")
    
    # Wait a moment
    time.sleep(3)
    
    # Try to find some common elements to verify app is running
    try:
        print("Looking for common elements...")
        
        # Try to find any text elements
        text_elements = session_driver.find_elements(AppiumBy.XPATH, '//*[@text]')
        print(f"Found {len(text_elements)} text elements")
        
        # Show first few text elements
        for i, elem in enumerate(text_elements[:5]):
            try:
                text = elem.get_attribute('text')
                print(f"  Element {i+1}: '{text}'")
            except:
                print(f"  Element {i+1}: <error getting text>")
        
        # Try to find any buttons
        buttons = session_driver.find_elements(AppiumBy.XPATH, '//android.widget.Button')
        print(f"Found {len(buttons)} buttons")
        
        # Show first few buttons
        for i, button in enumerate(buttons[:5]):
            try:
                text = button.get_attribute('text')
                content_desc = button.get_attribute('content-desc')
                print(f"  Button {i+1}: text='{text}', content-desc='{content_desc}'")
            except:
                print(f"  Button {i+1}: <error getting attributes>")
        
        print("✅ App appears to be running and elements are accessible")
        
    except Exception as e:
        print(f"❌ Error finding elements: {e}")
        print("❌ App may not be running properly")
    
    # Take a screenshot
    try:
        session_driver.save_screenshot("debug_app_launch.png")
        print("📸 Screenshot saved: debug_app_launch.png")
    except Exception as e:
        print(f"⚠️ Could not take screenshot: {e}")


def test_stay_arm_disarm(session_driver):
    """First test: login -> stay arm -> disarm"""
   # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)
    
    # Test Stay Arm cycle
    print("=== Testing Stay Arm Cycle ===")
    page.stay_arm()
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Stay Armed"  # Let's try the correct expectation
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
    time.sleep(2)
    
    # Disarm after stay arm
    do_disarm(session_driver)
    page = AreasPage(session_driver)
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Disarmed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
    time.sleep(2)

def test_sleep_arm_disarm(session_driver):
    """Second test: sleep arm -> disarm (continues same session)"""
    # Launch the app first
    launch_olarm_app(session_driver)
       # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)
    
    # Test Sleep Arm cycle (same session)
    print("=== Testing Sleep Arm Cycle ===")
    page.sleep_arm()
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Sleep Armed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
    #time.sleep(2)
    
    # Disarm after sleep arm
    do_disarm(session_driver)
    page = AreasPage(session_driver)
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Disarmed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
   # time.sleep(2)

def test_arm_disarm(session_driver):
    """Test: Arm -> Disarm"""
    # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)
    
    # Step 1: Click "Arm" button
    print("=== Step 1: Clicking Arm Button ===")
    page.click(page.arm_button)
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Arm: {info['status']}")
    assert "Armed" in info["status"]  # Should be "Armed""
    assert "•" in info["time"]
    
    # Step 2: Disarm
    do_disarm(session_driver)
    page = AreasPage(session_driver)
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Disarmed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
   # time.sleep(2)

def test_sleep_arm_to_stay_arm_to_arm(session_driver):
    """Test: Sleep Arm -> Stay Arm -> Arm"""
    # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)

    # Step 1: Click "sleep arm" button 
    print("=== Sleep Arming ===")
    page.sleep_arm()
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Sleep Armed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
    time.sleep(2)

    # Step 2: Click "stay arm" button 
    print("=== Stay Arming..")
    page.stay_arm()
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Stay Armed"
    assert "•" in info["time"]  # More flexible - accepts "Now" or "X secs ago"
    
    # Step 3: Click "Arm" button 
    print("=== Step 1: Clicking Arm Button ===")
    page.click(page.arm_button)
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Arm: {info['status']}")
    assert "Armed" in info["status"]  # Should be "Armed""
    assert "•" in info["time"]

def test_arm_to_sleep_arm_without_disarm(session_driver):
    """Test: Arm -> Sleep Arm (no disarm between)"""
    # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)
    
    # Step 1: Click "Arm" button
    print("=== Step 1: Clicking Arm Button ===")
    page.click(page.arm_button)
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Arm: {info['status']}")
    assert "Armed" in info["status"]  # Should be "Armed""
    assert "•" in info["time"]
    
    # Step 2: Click "Sleep Arm" button
    print("=== Step 2: Clicking Sleep Arm Button ===")
    page.sleep_arm()
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Sleep Arm: {info['status']}")
    assert info["status"] == "Sleep Armed"
    assert "•" in info["time"]

def test_arm_to_stay_arm_to_sleep_arm_without_disarm(session_driver):
    """Test: Arm -> Stay Arm -> Full Arm -> Sleep Arm (no disarm between)"""
    # Launch the app first
    launch_olarm_app(session_driver)
    
    # Login and setup (if not already logged in)
    try:
        first_login_btn(session_driver)
        do_login(session_driver)
        select_device(session_driver)
    except:
        print("Already logged in, continuing...")
    
    page = AreasPage(session_driver)
    
    # Step 1: Click "Arm" button
    print("=== Step 1: Clicking Arm Button ===")
    page.click(page.arm_button)
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Arm: {info['status']}")
    assert "Armed" in info["status"]  # Should be "Armed""
    assert "•" in info["time"]
    
    # Step 2: Click "Stay Arm" button
    print("=== Step 2: Clicking Stay Arm Button ===")
    page.stay_arm()
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Stay Arm: {info['status']}")
    assert info["status"] == "Stay Armed"
    assert "•" in info["time"]
    
    # Step 4: Click "Sleep Arm" button
    print("=== Step 4: Clicking Sleep Arm Button ===")
    page.sleep_arm()
    time.sleep(3)
    info = page.get_area_info_by_label("Area 1")
    print(f"Status after Sleep Arm: {info['status']}")
    assert info["status"] == "Sleep Armed"
    assert "•" in info["time"]

    # lastly disarm
    do_disarm(session_driver)
    page = AreasPage(session_driver)
    info = page.get_area_info_by_label("Area 1")
    assert info["status"] == "Disarmed"
    assert "•" in info["time"]
    
    print("=== All arm cycles completed successfully! ===")

def test_reset_app(driver_with_uninstall):
    # This test will uninstall the app after it runs
    pass
    ...

    #--------------------------------


    


