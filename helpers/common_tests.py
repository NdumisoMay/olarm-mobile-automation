import time

from appium.webdriver.common.appiumby import AppiumBy

from pages.add_device_page import AddDevicePage
from pages.devices_page import DevicesPage
from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.areas_page import AreasPage
from pages.logout_page import LogOutPage
from utils.data_reader import read_test_data, read_device_details


def handle_notification_permission_popup(driver, timeout=5):
    """
    Handle notification permission popup by allowing notifications
    
    Args:
        driver: Appium WebDriver instance
        timeout (int): Timeout in seconds to wait for permission popup
        
    Returns:
        bool: True if handled or no popup found, False if error
    """
    import time
    try:
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Look for notification permission dialog
                permission_selectors = [
                    'new UiSelector().text("Allow Olarm to send you notifications?")',
                    'new UiSelector().textContains("Allow").textContains("to send you notifications")',
                    'new UiSelector().textContains("notifications")',
                    'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_message")'
                ]
                
                for selector in permission_selectors:
                    try:
                        permission_dialog = driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR, 
                            selector
                        )
                        if permission_dialog.is_displayed():
                            print("✅ Found notification permission dialog")
                            
                            # Look for "Allow" button and click it
                            allow_selectors = [
                                'new UiSelector().text("Allow")',
                                'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")',
                                'new UiSelector().resourceId("android:id/button1")'
                            ]
                            
                            for allow_selector in allow_selectors:
                                try:
                                    allow_button = driver.find_element(
                                        AppiumBy.ANDROID_UIAUTOMATOR, 
                                        allow_selector
                                    )
                                    if allow_button.is_displayed():
                                        allow_button.click()
                                        print("✅ Clicked 'Allow' for notifications")
                                        time.sleep(1)
                                        return True
                                except Exception:
                                    continue
                            
                            print("⚠️ Found permission dialog but couldn't find Allow button")
                            return False
                            
                    except Exception:
                        continue
                
                # No permission dialog found, that's okay
                time.sleep(0.5)
                
            except Exception:
                pass
        
        print("ℹ️ No notification permission dialog found within timeout")
        return True
        
    except Exception as e:
        print(f"❌ Error handling notification permission: {e}")
        return True  # Don't fail the test for permission handling issues


def first_login_btn(driver):
    # Handle notification permission popup if it appears
    handle_notification_permission_popup(driver)
    
    # Try multiple locators for the login button to handle different app versions
    login_button_locators = [
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Login")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("login-button")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("btn-login")'),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Login")'),
        (AppiumBy.ACCESSIBILITY_ID, 'Login'),
        (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Login"]'),
        (AppiumBy.XPATH, '//android.widget.Button[@text="Login"]'),
        (AppiumBy.XPATH, '//*[@text="Login"]'),
        (AppiumBy.XPATH, '//*[@content-desc="Login"]')
    ]
    
    login_button_found = False
    for i, locator in enumerate(login_button_locators):
        try:
            print(f"🔍 Trying login button locator {i+1}: {locator}")
            element = driver.find_element(*locator)
            if element.is_displayed():
                print(f"✅ Found login button with locator {i+1}: {locator}")
                element.click()
                login_button_found = True
                break
        except Exception as e:
            print(f"❌ Locator {i+1} failed: {e}")
            continue
    
    if not login_button_found:
        print("❌ Could not find login button with any locator")
        # Take a screenshot for debugging
        try:
            driver.save_screenshot("login_button_not_found.png")
            print("📸 Screenshot saved: login_button_not_found.png")
        except Exception as e:
            print(f"⚠️ Could not take screenshot: {e}")
        raise Exception("Login button not found with any locator")
    
    print("✅ Login button clicked successfully")


def do_login(driver):
    credentials = read_test_data("valid_user")
    login_page = LoginPage(driver)
    login_page.login(credentials["username"], credentials["password"])

def select_device(driver):
    device_list = DevicesPage(driver)
    device_list.select_device()

#logout
def do_logout(driver):
    log_out = LogOutPage(driver)
    log_out.logout_user()
    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")

def do_logout_my_devices(driver):
    log_out = LogOutPage(driver)
    log_out.logout_my_devices()
    expected_text = "Login"
    login_button_locator = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Login")'
    )

    element = driver.find_element(*login_button_locator)
    actual_text = element.get_attribute("contentDescription")

    assert actual_text == expected_text, f"❌ Expected '{expected_text}', but got '{actual_text}'"
    print("✅ 'Login' button is visible with correct label.")

#Add device flow common tests

def do_add_olarm_device_btn(driver):
    first_login_btn(driver)
    do_login(driver)
    add_device_btn = AddDevicePage(driver)
    # Scroll to the element by its content-description before clicking it
    add_device_btn.scroll_to_description("Add Olarm Device")
    #time.sleep(1.5)
    add_device_btn.click_add_device()

    # new UiSelector().text("Scan the QR code on the back of your Olarm device.")


def do_click_serial_btn(driver):
    click_serial_btn = AddDevicePage(driver)
    click_serial_btn.click_serial_button()


def do_capture_device_details(driver):
    valid_device_details = read_device_details("valid_device")
    add_device = AddDevicePage(driver)
    add_device.type_device_details(valid_device_details["serial"], valid_device_details["verification_code"])


def do_add_device_name(driver):
    valid_device_name = read_device_details("name_device")
    add_device_name = AddDevicePage(driver)
    add_device_name.name_device(valid_device_name["name_of_device"])

def do_disarm(driver):
   # do_login(driver)
    #select_device(driver)
    areas_page = AreasPage(driver)
    areas_page.disarm_panel()
    time.sleep(5)  # Allow time for UI to reflect state change

def do_login_with_classic_tokens(driver):
    credentials = read_test_data("valid_user")
    login_page = LoginPage(driver)
    login_page.old_app_login(credentials["username"], credentials["password"])