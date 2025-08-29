import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class BurgerMenuPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    #identify drawer menu elements
    view_profile = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("View Profile")')
    device_status = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Device Status")')
    logout = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Logout")')

    profile_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Account")')
    account_setup_text = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Account setup")')
    account_setup_back_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("")')

    drawer_menu = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(1)')

    device_notifications_menu_item = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Device Notifications")')

    device_notifications_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Device Notifications")')
    device_notifications_back_arrow = (AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Navigate up') or contains(@content-desc, 'Back')]")
    dn_arm_partial_arm_disarm_notifications = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Arm, Partial Arm and Disarm")')
    reminder_and_alerts = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Reminders & Alerts")')
    cant_get_notifications = (AppiumBy.ACCESSIBILITY_ID, 'Can\'t get notifications?')
    cant_get_notifications_notification_and_alerts_page = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Notification & Alerts")')
    notification_and_alerts_close_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("")')

    switch_arm_partial_arm_disarm_notifications = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Switch").instance(0)')

    turn_off_notifications_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Turn off these notifications?")')
    turn_off_notifications_warning_msg = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Warning: Disabling notifications means you won\'t receive important security alerts or system updates from your alarm system. Do you want to continue?")')
    turn_off_notifications_confirm_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button")')
    turn_off_notifications_cancel_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Cancel")')

    #identify device status elements
    panel_ac_power = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Panel AC Power")')
    panel_ac_power_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ON").instance(0)')
    panel_battery_power = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Panel Battery Power")')
    panel_battery_power_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("GOOD").instance(0)')
    power_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Power input")')
    power_input_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("ON").instance(1)')
    backup_power = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Backup power")')
    backup_power_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("GOOD").instance(1)')
    antenna = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Antenna")')
    antenna_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("INTERNAL")')
    cellular_signal_strength = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Cellular signal strength")')
    cellular_signal_strength_value = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("STRONG")')

    back_arrow_device_status = (AppiumBy.ACCESSIBILITY_ID, 'Back')

    terms_of_service = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Terms of service")')

    terms_of_service_page_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Terms & conditions")')
    terms_of_service_instruction = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Read the terms and conditions for using Olarm’s products, services, and website in the UK. Learn about your rights, responsibilities, and usage policies.")')
    terms_of_service_body = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView").instance(4)')


   


    #click drawer menu elements
    def click_drawer_menu(self):
        """Click the Drawer Menu button"""
        self.click(self.drawer_menu)
        time.sleep(1)

    def click_view_profile(self):
        """Click the View Profile button"""
        self.click(self.view_profile)
        time.sleep(1)

    def click_account_setup_back_btn(self):
        """Click the Account setup back button"""
        self.click(self.account_setup_back_btn)
        time.sleep(1)

    def click_back_status_page(self):
        """Click the Back arrow button"""
        self.click(self.back_arrow_device_status)
        time.sleep(1)

    def click_device_status(self):
        """Click the Device status button"""
        self.click(self.device_status)
        time.sleep(1)

    def click_device_notifications(self):   
        """Click the Device notifications button"""
        self.click(self.device_notifications_menu_item)
        time.sleep(1)
    
    def dismiss_device_notifications_modal(self):
        """Dismiss the Device Notifications bottom sheet modal using multiple methods"""
        try:
            print("🔙 Attempting to dismiss Device Notifications modal...")
            
            # Method 1: Try the back arrow button
            try:
                self.click(self.device_notifications_back_arrow)
                print("✅ Dismissed modal using back arrow")
                time.sleep(1)
                return
            except Exception as e1:
                print(f"❌ Back arrow failed: {e1}")
            
            # Method 2: Use Android back button
            try:
                self.driver.back()
                print("✅ Dismissed modal using Android back button")
                time.sleep(1)
                return
            except Exception as e2:
                print(f"❌ Android back button failed: {e2}")
            
            # Method 3: Swipe down to dismiss (bottom sheet gesture)
            try:
                screen_size = self.driver.get_window_size()
                width = screen_size['width']
                height = screen_size['height']
                
                start_x = width // 2
                start_y = height // 2
                end_x = width // 2
                end_y = height - 100
                
                self.driver.swipe(start_x, start_y, end_x, end_y, 500)
                print("✅ Dismissed modal using swipe down gesture")
                time.sleep(1)
                return
            except Exception as e3:
                print(f"❌ Swipe down failed: {e3}")
            
            # Method 4: Tap outside the modal (in the grayed out area)
            try:
                screen_size = self.driver.get_window_size()
                x = screen_size['width'] // 2  # Center horizontally
                y = 100  # Upper area above the modal
                self.driver.tap([(x, y)])
                print("✅ Dismissed modal by tapping outside")
                time.sleep(1)
                return
            except Exception as e4:
                print(f"❌ Tap outside failed: {e4}")
            
            raise Exception("All methods failed to dismiss Device Notifications modal")
            
        except Exception as e:
            print(f"❌ Could not dismiss Device Notifications modal: {e}")
            raise

    def click_close_modal(self):
        """Click the outside modal"""
        self.click(self.click_outside_modal)
        time.sleep(1)

    def click_cant_get_notifications_link(self):
        """Click the Cant get notifications link"""
        self.click(self.cant_get_notifications)
        time.sleep(1)

    def click_notification_and_alerts_close_btn(self):
        """Click the Notification and alerts close button"""
        self.click(self.notification_and_alerts_close_btn)
        time.sleep(1)

    def click_toggle_to_disable_arm_partial_arm_disarm_notifications(self): 
        """Click the toggle to disable arm, partial arm and disarm notifications"""
        self.click(self.switch_arm_partial_arm_disarm_notifications)
        time.sleep(1)

    def click_toggle_to_enable_arm_partial_arm_disarm_notifications(self):
        """Click the toggle to enable arm, partial arm and disarm notifications"""
        self.click(self.switch_arm_partial_arm_disarm_notifications)
        time.sleep(1)

    def click_turn_off_notifications_confirm_btn(self):
        """Click the Turn off notifications confirm button"""
        self.click(self.turn_off_notifications_confirm_btn)
        time.sleep(1)

    def click_turn_off_notifications_cancel_btn(self):
        """Click the Turn off notifications cancel button"""
        self.click(self.turn_off_notifications_cancel_btn)
        time.sleep(1)

    def tap_outside_modal(self):
        # Get screen size
        screen_size = self.driver.get_window_size()
        
        # Tap on the gray area (upper part of screen)
        x = screen_size['width'] // 2  # Center horizontally
        y = 100  # Upper area above the modal
        self.driver.tap([(x, y)])

    def click_terms_of_service(self):
        """Click the Terms of service button"""
        self.click(self.terms_of_service)
        time.sleep(1)
    
    def navigate_back_from_terms_of_service(self):
        """Navigate back from Terms of Service webview to app"""
        try:
            print("🔙 Attempting to navigate back from Terms of Service...")
            # Method 1: Use Android back button
            self.driver.back()
            time.sleep(2)
            print("✅ Successfully navigated back using driver.back()")
        except Exception as e1:
            print(f"❌ driver.back() failed: {e1}")
            try:
                # Method 2: Use back keycode
                self.driver.press_keycode(4)  # KEYCODE_BACK
                time.sleep(2)
                print("✅ Successfully navigated back using keycode")
            except Exception as e2:
                print(f"❌ keycode back failed: {e2}")
                try:
                    # Method 3: Context switch if in webview
                    if self.driver.current_context != "NATIVE_APP":
                        self.driver.switch_to.context("NATIVE_APP")
                        print("✅ Switched back to native app context")
                    else:
                        print("⚠️ Already in native app context")
                except Exception as e3:
                    print(f"❌ Context switch failed: {e3}")
                    # Method 4: Edge swipe gesture as last resort
                    try:
                        screen_size = self.driver.get_window_size()
                        width = screen_size['width']
                        height = screen_size['height']
                        self.driver.swipe(0, height // 2, width // 4, height // 2, 300)
                        time.sleep(2)
                        print("✅ Successfully navigated back using swipe gesture")
                    except Exception as e4:
                        print(f"❌ All navigation methods failed: {e4}")
                        raise Exception("Could not navigate back from Terms of Service")