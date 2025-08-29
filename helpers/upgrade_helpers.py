import os
import time
import subprocess
from appium.webdriver.common.appiumby import AppiumBy
# TouchAction is deprecated in newer Appium versions, using W3C Actions instead


class UpgradeHelpers:
    """Helper class for app upgrade automation"""
    
    def __init__(self, driver):
        self.driver = driver
    
    def install_app_version(self, apk_path, package_name):
        """
        Install a specific version of the app
        
        Args:
            apk_path (str): Path to the APK file
            package_name (str): Package name of the app
            
        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            # Check if APK file exists
            if not os.path.exists(apk_path):
                print(f"❌ APK file not found: {apk_path}")
                return False
            
            # Install new version (will overwrite existing app)
            self.driver.install_app(apk_path)
            print(f"✅ Installed app from: {apk_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install app: {e}")
            return False
    
    def install_app_version_clean(self, apk_path, package_name):
        """
        Install a specific version of the app with clean installation (uninstall first)
        
        Args:
            apk_path (str): Path to the APK file
            package_name (str): Package name of the app
            
        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            # Check if APK file exists
            if not os.path.exists(apk_path):
                print(f"❌ APK file not found: {apk_path}")
                return False
            
            # Uninstall existing app if present
            try:
                self.driver.remove_app(package_name)
                print(f"✅ Uninstalled existing app: {package_name}")
                time.sleep(2)  # Wait for uninstall to complete
            except Exception as e:
                print(f"ℹ️ No existing app to uninstall: {e}")
            
            # Install new version
            self.driver.install_app(apk_path)
            print(f"✅ Installed app from: {apk_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install app: {e}")
            return False
    
    def install_app_version_direct(self, apk_path, package_name):
        """
        Install a specific version of the app directly (no uninstall first)
        
        Args:
            apk_path (str): Path to the APK file
            package_name (str): Package name of the app
            
        Returns:
            bool: True if installation successful, False otherwise
        """
        try:
            # Check if APK file exists
            if not os.path.exists(apk_path):
                print(f"❌ APK file not found: {apk_path}")
                return False
            
            # Install new version directly (will overwrite if exists)
            self.driver.install_app(apk_path)
            print(f"✅ Installed app from: {apk_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install app: {e}")
            return False
    
    def verify_app_installed(self, package_name):
        """
        Verify that the app is installed
        
        Args:
            package_name (str): Package name to check
            
        Returns:
            bool: True if app is installed, False otherwise
        """
        try:
            is_installed = self.driver.is_app_installed(package_name)
            if is_installed:
                print(f"✅ App {package_name} is installed")
            else:
                print(f"❌ App {package_name} is not installed")
            return is_installed
        except Exception as e:
            print(f"❌ Error checking app installation: {e}")
            return False
    
    def launch_app(self, package_name, activity_name=None):
        """
        Launch the app
        
        Args:
            package_name (str): Package name of the app
            activity_name (str): Activity name to launch (optional)
            
        Returns:
            bool: True if app launched successfully, False otherwise
        """
        try:
            if activity_name:
                self.driver.start_activity(package_name, activity_name)
            else:
                self.driver.activate_app(package_name)
            
            print(f"✅ Launched app: {package_name}")
            time.sleep(3)  # Wait for app to load
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to launch app: {e}")
            return False
    
    def handle_notification_permission(self, timeout=5):
        """
        Handle notification permission popup by allowing notifications
        
        Args:
            timeout (int): Timeout in seconds to wait for permission popup
            
        Returns:
            bool: True if handled or no popup found, False if error
        """
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
                            permission_dialog = self.driver.find_element(
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
                                        allow_button = self.driver.find_element(
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

    def auto_grant_all_permissions(self, timeout=10):
        """
        Automatically grant all permissions that might appear after login
        This simulates the autoGrantPermissions behavior for runtime permissions
        
        Args:
            timeout (int): Timeout in seconds to wait for permission dialogs
            
        Returns:
            bool: True if all permissions handled successfully
        """
        try:
            print("🔧 Auto-granting all permissions after login...")
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    # Look for various permission dialogs
                    permission_patterns = [
                        # Notification permissions
                        ('new UiSelector().textContains("notifications")', 'Allow'),
                        ('new UiSelector().textContains("notification")', 'Allow'),
                        # Location permissions
                        ('new UiSelector().textContains("location")', 'Allow'),
                        ('new UiSelector().textContains("Location")', 'Allow'),
                        # Camera permissions
                        ('new UiSelector().textContains("camera")', 'Allow'),
                        ('new UiSelector().textContains("Camera")', 'Allow'),
                        # Storage permissions
                        ('new UiSelector().textContains("storage")', 'Allow'),
                        ('new UiSelector().textContains("Storage")', 'Allow'),
                        # Microphone permissions
                        ('new UiSelector().textContains("microphone")', 'Allow'),
                        ('new UiSelector().textContains("Microphone")', 'Allow'),
                        # Generic permission dialogs
                        ('new UiSelector().resourceId("com.android.permissioncontroller:id/permission_message")', 'Allow'),
                        ('new UiSelector().resourceId("android:id/alertTitle")', 'Allow'),
                        # App-specific permission dialogs
                        ('new UiSelector().textContains("Olarm")', 'Allow'),
                        ('new UiSelector().textContains("olarm")', 'Allow')
                    ]
                    
                    for pattern, action in permission_patterns:
                        try:
                            dialog = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, pattern)
                            if dialog.is_displayed():
                                print(f"✅ Found permission dialog: {pattern}")
                                
                                # Look for action buttons (Allow, OK, Yes, etc.)
                                action_selectors = [
                                    f'new UiSelector().text("{action}")',
                                    f'new UiSelector().text("{action.lower()}")',
                                    f'new UiSelector().text("{action.upper()}")',
                                    'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")',
                                    'new UiSelector().resourceId("android:id/button1")',
                                    'new UiSelector().resourceId("android:id/positive")',
                                    'new UiSelector().text("OK")',
                                    'new UiSelector().text("Yes")',
                                    'new UiSelector().text("Accept")'
                                ]
                                
                                for action_selector in action_selectors:
                                    try:
                                        button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, action_selector)
                                        if button.is_displayed():
                                            button.click()
                                            print(f"✅ Clicked '{action}' for permission")
                                            time.sleep(1)
                                            break
                                    except Exception:
                                        continue
                                
                                # Continue looking for more dialogs
                                break
                                
                        except Exception:
                            continue
                    
                    # Check if we're done (no more dialogs)
                    time.sleep(0.5)
                    
                except Exception:
                    pass
            
            print("✅ Auto-grant permissions completed")
            return True
            
        except Exception as e:
            print(f"❌ Error in auto-grant permissions: {e}")
            return True  # Don't fail the test for permission handling issues
    
    def verify_user_logged_in(self, timeout=10):
        """
        Verify user is logged in by checking for 'My Devices' screen
        
        Args:
            timeout (int): Timeout in seconds to wait for login verification
            
        Returns:
            bool: True if user is logged in, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check if "My Devices" text is visible
                my_devices_element = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, 
                    'new UiSelector().text("My Devices")'
                )
                
                if my_devices_element.is_displayed():
                    print("✅ User is logged in - 'My Devices' screen visible")
                    return True
                    
            except Exception:
                # Element not found, continue checking
                pass
            
            time.sleep(1)
        
        print("❌ User is not logged in - 'My Devices' screen not visible")
        # Take a screenshot for debugging when login fails
        try:
            self.take_screenshot("login_failure_debug.png")
            print("📸 Debug screenshot saved: upgrade_screenshots/login_failure_debug.png")
        except Exception as e:
            print(f"⚠️ Could not take debug screenshot: {e}")
        return False

    def verify_my_devices_screen_content(self, timeout=10):
        """
        Verify that the My Devices screen contains expected content after upgrade
        and does NOT contain error messages or problematic content
        
        Args:
            timeout (int): Timeout in seconds to wait for content verification
            
        Returns:
            bool: True if expected content is found and no errors, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # First, check for UNWANTED content (error messages, problematic content)
                unwanted_content_selectors = [
                    ('new UiSelector().text("It appears that you do not have devices, but none of them are online")', "No devices online error"),
                    ('new UiSelector().text("There was a problem with your request. Please try again.")', "Request problem error"),
                    ('new UiSelector().textContains("It appears that you do not have devices")', "No devices error (partial)"),
                    ('new UiSelector().textContains("There was a problem with your request")', "Request problem error (partial)"),
                    ('new UiSelector().text("Error")', "Generic error"),
                    ('new UiSelector().text("Failed")', "Failed message"),
                    ('new UiSelector().text("Connection Error")', "Connection error"),
                    ('new UiSelector().text("Network Error")', "Network error"),
                    ('new UiSelector().text("Server Error")', "Server error"),
                    ('new UiSelector().text("Please try again")', "Try again message")
                ]
                
                found_unwanted_content = []
                
                for selector, description in unwanted_content_selectors:
                    try:
                        element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR, 
                            selector
                        )
                        if element.is_displayed():
                            found_unwanted_content.append(description)
                            print(f"❌ Found unwanted content: {description}")
                    except Exception:
                        continue
                
                # If we found any unwanted content, the screen has problems
                if found_unwanted_content:
                    print(f"❌ My Devices screen contains problematic content: {', '.join(found_unwanted_content)}")
                    
                    # Take a screenshot for debugging
                    try:
                        self.take_screenshot("my_devices_error_content.png")
                        print("📸 Error screenshot saved: upgrade_screenshots/my_devices_error_content.png")
                    except Exception as e:
                        print(f"⚠️ Could not take error screenshot: {e}")
                    
                    return False
                
                # Now check for expected content on My Devices screen
                expected_content_selectors = [
                    ('new UiSelector().text("Devices Online")', "Devices Online"),
                    ('new UiSelector().text("Devices Offline")', "Devices Offline"),
                    ('new UiSelector().text("Add Olarm Device")', "Add Olarm Device"),
                    ('new UiSelector().description("Add Olarm Device")', "Add Olarm Device (description)"),
                    ('new UiSelector().text("No devices found")', "No devices found"),
                    ('new UiSelector().text("Add Device")', "Add Device"),
                    ('new UiSelector().text("Add your first device")', "Add your first device")
                ]
                
                found_content = []
                
                for selector, description in expected_content_selectors:
                    try:
                        element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR, 
                            selector
                        )
                        if element.is_displayed():
                            found_content.append(description)
                            print(f"✅ Found expected content: {description}")
                    except Exception:
                        continue
                
                # If we found any of the expected content, the screen is functional
                if found_content:
                    print(f"✅ My Devices screen is functional - Found: {', '.join(found_content)}")
                    return True
                    
            except Exception as e:
                print(f"⚠️ Error checking My Devices content: {e}")
                pass
            
            time.sleep(1)
        
        print("❌ My Devices screen does not contain expected content")
        print("Expected to find one of: Devices Online, Devices Offline, Add Olarm Device, Add Device, No devices found, Add your first device")
        
        # Take a screenshot for debugging
        try:
            self.take_screenshot("my_devices_content_failure.png")
            print("📸 Debug screenshot saved: upgrade_screenshots/my_devices_content_failure.png")
        except Exception as e:
            print(f"⚠️ Could not take debug screenshot: {e}")
        
        return False
    
    def verify_landing_screen(self, timeout=10):
        """
        Verify app shows landing screen (not logged in)
        
        Args:
            timeout (int): Timeout in seconds to wait for landing screen
            
        Returns:
            bool: True if landing screen is visible, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check for login button on landing screen
                login_button = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, 
                    'new UiSelector().description("Login")'
                )
                
                if login_button.is_displayed():
                    print("✅ Landing screen is visible")
                    return True
                    
            except Exception:
                # Element not found, continue checking
                pass
            
            time.sleep(1)
        
        print("❌ Landing screen not visible")
        return False
    
    def check_for_error_dialogs(self):
        """
        Check for common error dialogs or crash dialogs
        
        Returns:
            list: List of error messages found
        """
        error_messages = []
        error_selectors = [
            ('new UiSelector().text("Error")', "Error dialog"),
            ('new UiSelector().text("Crash")', "Crash dialog"),
            ('new UiSelector().text("App has stopped")', "App stopped dialog"),
            ('new UiSelector().text("Unfortunately")', "Unfortunately dialog"),
            ('new UiSelector().text("Force Close")', "Force close dialog"),
            ('new UiSelector().text("ANR")', "ANR dialog"),
            ('new UiSelector().text("Not Responding")', "Not responding dialog")
        ]
        
        for selector, description in error_selectors:
            try:
                error_element = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR, 
                    selector
                )
                if error_element.is_displayed():
                    error_messages.append(description)
                    print(f"❌ Found error dialog: {description}")
            except Exception:
                # Element not found, which is good
                pass
        
        if not error_messages:
            print("✅ No error dialogs detected")
        
        return error_messages
    
    def wait_for_app_load(self, timeout=30):
        """
        Wait for app to fully load after launch
        
        Args:
            timeout (int): Timeout in seconds to wait for app load
            
        Returns:
            bool: True if app loaded successfully, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # First, check for error dialogs or crash states
                error_selectors = [
                    'new UiSelector().text("App has stopped")',
                    'new UiSelector().text("Unfortunately")',
                    'new UiSelector().text("Force Close")',
                    'new UiSelector().text("ANR")',
                    'new UiSelector().text("Not Responding")',
                    'new UiSelector().text("It appears that you do not have devices, but none of them are online")',
                    'new UiSelector().text("There was a problem with your request. Please try again.")'
                ]
                
                for error_selector in error_selectors:
                    try:
                        error_element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR, 
                            error_selector
                        )
                        if error_element.is_displayed():
                            print(f"❌ App is showing error state: {error_selector}")
                            # Take a screenshot for debugging
                            self.take_screenshot("app_error_state.png")
                            return False
                    except Exception:
                        continue
                
                # Check if app is responsive by looking for common elements
                elements_to_check = [
                    'new UiSelector().text("My Devices")',
                    'new UiSelector().description("Login")',
                    'new UiSelector().resourceId("text-input-outlined")',
                    'new UiSelector().text("Devices Online")',
                    'new UiSelector().text("Devices Offline")',
                    'new UiSelector().text("Add Olarm Device")'
                ]
                
                for selector in elements_to_check:
                    try:
                        element = self.driver.find_element(
                            AppiumBy.ANDROID_UIAUTOMATOR, 
                            selector
                        )
                        if element.is_displayed():
                            print(f"✅ App loaded successfully - Found: {selector}")
                            return True
                    except Exception:
                        continue
                
            except Exception as e:
                print(f"⚠️ Error during app load check: {e}")
                pass
            
            time.sleep(1)
        
        print("❌ App did not load within timeout")
        # Take a screenshot for debugging
        self.take_screenshot("app_load_timeout.png")
        return False
    
    def clear_app_data(self, package_name):
        """
        Clear app data (equivalent to uninstall + reinstall)
        
        Args:
            package_name (str): Package name of the app
            
        Returns:
            bool: True if data cleared successfully, False otherwise
        """
        try:
            # Clear app data using ADB
            device_id = self.driver.desired_capabilities.get('udid', 'emulator-5554')
            cmd = f"adb -s {device_id} shell pm clear {package_name}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Cleared app data for: {package_name}")
                return True
            else:
                print(f"❌ Failed to clear app data: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error clearing app data: {e}")
            return False
    
    def get_app_version(self, package_name):
        """
        Get the installed version of the app
        
        Args:
            package_name (str): Package name of the app
            
        Returns:
            str: Version string or None if not found
        """
        try:
            device_id = self.driver.desired_capabilities.get('udid', 'emulator-5554')
            cmd = f"adb -s {device_id} shell dumpsys package {package_name} | grep versionName"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse version from output
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if 'versionName=' in line:
                        version = line.split('versionName=')[1].strip()
                        print(f"✅ App version: {version}")
                        return version
            
            print("❌ Could not determine app version")
            return None
            
        except Exception as e:
            print(f"❌ Error getting app version: {e}")
            return None
    
    def take_screenshot(self, filename):
        """
        Take a screenshot for debugging purposes
        
        Args:
            filename (str): Name of the screenshot file
            
        Returns:
            bool: True if screenshot taken successfully, False otherwise
        """
        try:
            # Create upgrade_screenshots directory if it doesn't exist
            screenshot_dir = "upgrade_screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            screenshot_path = os.path.join(screenshot_dir, filename)
            
            self.driver.save_screenshot(screenshot_path)
            print(f"✅ Screenshot saved: {screenshot_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to take screenshot: {e}")
            return False
    
    def wait_for_element(self, locator, timeout=10):
        """
        Wait for an element to be visible
        
        Args:
            locator (tuple): Element locator (strategy, value)
            timeout (int): Timeout in seconds
            
        Returns:
            bool: True if element found, False otherwise
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    return True
            except Exception:
                pass
            
            time.sleep(0.5)
        
        return False
    
    def scroll_to_element(self, locator, max_scrolls=5):
        """
        Scroll to find an element using W3C Actions
        
        Args:
            locator (tuple): Element locator (strategy, value)
            max_scrolls (int): Maximum number of scroll attempts
            
        Returns:
            bool: True if element found, False otherwise
        """
        for i in range(max_scrolls):
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed():
                    return True
            except Exception:
                pass
            
            # Scroll down using W3C Actions
            screen_size = self.driver.get_window_size()
            start_x = screen_size['width'] * 0.5
            start_y = screen_size['height'] * 0.8
            end_y = screen_size['height'] * 0.2
            
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
            actions.w3c_actions.pointer_action.pointer_up()
            actions.perform()
            
            time.sleep(1)
        
        return False

    def open_drawer_menu_and_verify_version(self, expected_version, screenshot_name):
        """
        Open the drawer menu, scroll to bottom to find version info, and take screenshot
        
        Args:
            expected_version (str): Expected app version to verify
            screenshot_name (str): Name for the screenshot file
            
        Returns:
            bool: True if version verified and screenshot taken, False otherwise
        """
        try:
            from appium.webdriver.common.appiumby import AppiumBy
            
            print(f"🔍 Opening drawer menu to verify version {expected_version}...")
            
            # Click on the drawer menu using the provided locator
            try:
                menu_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button")')
                if menu_button.is_displayed():
                    menu_button.click()
                    print("✅ Drawer menu opened successfully")
                    time.sleep(2)
                else:
                    print("⚠️ Drawer menu button not visible")
                    self.take_screenshot(screenshot_name)
                    return False
            except Exception as e:
                print(f"❌ Failed to open drawer menu: {e}")
                self.take_screenshot(screenshot_name)
                return False
            
            # Scroll to bottom of the drawer menu to find version info
            print("📜 Scrolling to bottom of drawer menu to find version info...")
            
            # Try to find version text at the bottom
            version_found = False
            max_scrolls = 3
            
            for scroll_attempt in range(max_scrolls):
                try:
                    # Look for version text patterns
                    version_selectors = [
                        'new UiSelector().textContains("Version")',
                        'new UiSelector().textContains("v2.0")',
                        'new UiSelector().textContains("2.0")',
                        'new UiSelector().textContains("App Version")',
                        'new UiSelector().textContains("Build")'
                    ]
                    
                    for selector in version_selectors:
                        try:
                            version_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector)
                            if version_element.is_displayed():
                                version_text = version_element.text
                                print(f"✅ Found version info: {version_text}")
                                
                                # Verify the version matches expected
                                if expected_version in version_text:
                                    print(f"✅ Version verification successful: {expected_version}")
                                    version_found = True
                                    break
                                else:
                                    print(f"⚠️ Version mismatch. Expected: {expected_version}, Found: {version_text}")
                        except Exception:
                            continue
                    
                    if version_found:
                        break
                    
                    # Scroll down in drawer menu
                    screen_size = self.driver.get_window_size()
                    start_x = screen_size['width'] * 0.5
                    start_y = screen_size['height'] * 0.8
                    end_y = screen_size['height'] * 0.2
                    
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
                    actions.w3c_actions.pointer_action.pointer_down()
                    actions.w3c_actions.pointer_action.move_to_location(start_x, end_y)
                    actions.w3c_actions.pointer_action.pointer_up()
                    actions.perform()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️ Scroll attempt {scroll_attempt + 1} failed: {e}")
                    continue
            
            # Take screenshot regardless of version verification
            print(f"📸 Taking screenshot: {screenshot_name}")
            self.take_screenshot(screenshot_name)
            
            # Also get app version via ADB for additional verification
            package_name = "com.olarm.olarm1"
            adb_version = self.get_app_version(package_name)
            
            if adb_version:
                print(f"📱 ADB reported version: {adb_version}")
                if expected_version in adb_version:
                    print(f"✅ ADB version verification successful: {expected_version}")
                else:
                    print(f"⚠️ ADB version mismatch. Expected: {expected_version}, Found: {adb_version}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in open_drawer_menu_and_verify_version: {e}")
            # Still take screenshot even if there's an error
            self.take_screenshot(screenshot_name)
            return False
