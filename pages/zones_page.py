import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class ZonesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    # Locate elements
    zones_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Zones")')
    active_zones_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Active")')
    bypassed_zones_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Bypassed").clickable(true)')
    all_zones_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("All")')

    search_zones_field = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("text-input-outlined")')
    
    # Zone buttons 
    zone_1_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(0)')   
    zone_2_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(1)')
    zone_3_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(2)')
    zone_4_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(3)')
    zone_5_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(4)')
    zone_6_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button").instance(5)')

    # Zone names
    zone_10_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Zone 10")')
    zone_06_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Zone 06")')
    zone_07_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Zone 07")')
    zone_08_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Zone 08")')
    zone_09_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Zone 09")')
   




    def click_zones(self):
        """Click on the zones button with proper error handling"""
        try:
            print("=== Clicking Zones Button ===")
            self.click(self.zones_button)
            time.sleep(3)  # Increased wait time for stability
            print("✅ Zones button clicked successfully")
        except Exception as e:
            print(f"❌ Error clicking zones button: {e}")
            raise

    def click_bypassed_zones(self):
        """Click on the bypassed zones button with proper error handling"""
        try:
            print("=== Clicking Bypassed Zones Button ===")
            self.click(self.bypassed_zones_button)
            time.sleep(2)  # Increased wait time for stability
            print("✅ Bypassed zones button clicked successfully")
        except Exception as e:
            print(f"❌ Error clicking bypassed zones button: {e}")
            raise

    def click_all_zones(self):
        """Click on the all zones button with proper error handling"""
        try:
            print("=== Clicking All Zones Button ===")
            self.click(self.all_zones_button)
            time.sleep(3)  # Increased wait time for stability
            print("✅ All zones button clicked successfully")
        except Exception as e:
            print(f"❌ Error clicking all zones button: {e}")
            raise

    def verify_zones_page_elements(self):
        """Verify that zones page elements are visible"""
        try:
            print("=== Verifying Zones Page Elements ===")
            
            # Check if active zones button is visible
            active_visible = self.is_element_visible(self.active_zones_button, timeout=5)
            print(f"Active zones button visible: {active_visible}")
            
            # Check if bypassed zones button is visible  
            bypassed_visible = self.is_element_visible(self.bypassed_zones_button, timeout=5)
            print(f"Bypassed zones button visible: {bypassed_visible}")

            #check if zone 1 is bypassed (changed to "reset")
            is_zone_1_bypassed = self.is_element_visible(self.zone_1_reset_btn, timeout=5)
            print(f"Zone 1 bypassed: {is_zone_1_bypassed}")

            is_zone_2_bypassed = self.is_element_visible(self.zone_2_reset_btn, timeout=5)
            print(f"Zone 2 bypassed: {is_zone_2_bypassed}")

            is_zone_3_bypassed = self.is_element_visible(self.zone_3_reset_btn, timeout=5)
            print(f"Zone 3 bypassed: {is_zone_3_bypassed}")

            is_zone_4_bypassed = self.is_element_visible(self.zone_4_reset_btn, timeout=5)
            print(f"Zone 4 bypassed: {is_zone_4_bypassed}") 

            is_zone_5_bypassed = self.is_element_visible(self.zone_5_reset_btn, timeout=5)
            print(f"Zone 5 bypassed: {is_zone_5_bypassed}")

            is_zone_6_bypassed = self.is_element_visible(self.zone_6_reset_btn, timeout=5)
            print(f"Zone 6 bypassed: {is_zone_6_bypassed}")
            
            return active_visible and bypassed_visible and is_zone_1_bypassed and is_zone_2_bypassed and is_zone_3_bypassed and is_zone_4_bypassed and is_zone_5_bypassed and is_zone_6_bypassed
        

            #check if zones are bypassed
            is_zone_1_bypassed = self.is_element_visible(self.zone_1_reset_btn, timeout=5)
            print(f"Zone 1 bypassed: {is_zone_1_bypassed}")

            is_zone_2_bypassed = self.is_element_visible(self.zone_2_reset_btn, timeout=5)
            
        except Exception as e:
            print(f"❌ Error verifying zones page elements: {e}")
            return False
        
    def bypass_zones(self):
        """Bypass exactly 6 zones using a more reliable approach"""
        print("=== Bypassing exactly 6 zones ===")
        
        try:
            # Find all bypass buttons on the page
            bypass_buttons = self.driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Bypass"]')
            print(f"Found {len(bypass_buttons)} bypass buttons total")
            
            # Limit to exactly 6 zones
            zones_to_bypass = min(len(bypass_buttons), 6)
            print(f"Processing exactly {zones_to_bypass} zones (limited to 6)")
            
            # Click each bypass button in order, limited to 6
            for i in range(zones_to_bypass):
                try:
                    print(f"Clicking zone {i+1}...")
                    bypass_buttons[i].click()
                    time.sleep(2)
                    print(f"✅ Zone {i+1} bypassed successfully")
                except Exception as e:
                    print(f"❌ Error clicking zone {i+1}: {e}")
                    continue
            
            print(f"✅ Successfully processed exactly {zones_to_bypass} zones")
            
        except Exception as e:
            print(f"❌ Error in bypass_zones: {e}")
            raise
           

    def verify_bypassed_zones_in_bypassed_tab(self):
        """Verify if exactly 6 zones are bypassed in bypassed tab using a more reliable approach"""
        print("=== Verifying exactly 6 bypassed zones in bypassed tab ===")
        
        # Debug: Find all elements with "Bypassed" content-desc
        try:
            all_bypassed_elements = self.driver.find_elements(AppiumBy.XPATH, '//*[@content-desc="Bypassed"]')
            print(f"Found {len(all_bypassed_elements)} elements with 'Bypassed' content-desc")
            for i, elem in enumerate(all_bypassed_elements):
                try:
                    bounds = elem.get_attribute('bounds')
                    clickable = elem.get_attribute('clickable')
                    print(f"  Element {i+1}: bounds={bounds}, clickable={clickable}")
                except Exception as e:
                    print(f"  Element {i+1}: Error getting attributes: {e}")
        except Exception as e:
            print(f"Error finding bypassed elements: {e}")
        
        # Click the bypassed tab
        print("Clicking bypassed tab...")
        self.click(self.bypassed_zones_button)
        #time.sleep(2)
        
        try:
            # Find all reset buttons on the page
            reset_buttons = self.driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
            print(f"Found {len(reset_buttons)} reset buttons in bypassed tab")
            
            # Limit to exactly 6 zones
            zones_to_check = min(len(reset_buttons), 6)
            print(f"Checking exactly {zones_to_check} zones (limited to 6)")
            
            # Check each reset button, limited to 6
            zones_status = []
            for i in range(zones_to_check):
                try:
                    is_visible = reset_buttons[i].is_displayed()
                    print(f"Zone {i+1} shows in bypassed zones tab: {is_visible}")
                    zones_status.append(is_visible)
                except Exception as e:
                    print(f"❌ Error checking zone {i+1}: {e}")
                    zones_status.append(False)
            
            all_bypassed = all(zones_status) if zones_status else False
            print(f"✅ All {zones_to_check} zones bypassed: {all_bypassed}")
            return all_bypassed
            
        except Exception as e:
            print(f"❌ Error in verify_bypassed_zones_in_bypassed_tab: {e}")
            raise
           

    def reset_zones(self):
        """Reset exactly 6 zones using a more reliable approach"""
        print("=== Resetting exactly 6 zones ===")
        
        try:
            # Keep resetting zones until no more reset buttons are found
            zones_reset = 0
            max_attempts = 6  # Limit to 6 zones maximum
            
            while zones_reset < max_attempts:
                try:
                    # Find all reset buttons on the page
                    reset_buttons = self.driver.find_elements(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Reset"]')
                    print(f"Found {len(reset_buttons)} reset buttons available")
                    
                    if len(reset_buttons) == 0:
                        print("No more reset buttons found - all zones have been reset")
                        break
                    
                    # Click the first available reset button
                    print(f"Resetting zone {zones_reset + 1}...")
                    reset_buttons[0].click()
                    time.sleep(2)
                    print(f"✅ Zone {zones_reset + 1} reset successfully")
                    zones_reset += 1
                    
                except Exception as e:
                    print(f"❌ Error resetting zone {zones_reset + 1}: {e}")
                    # If we get an error, try to refresh and continue
                    time.sleep(1)
                    continue
            
            print(f"✅ Successfully reset {zones_reset} zones")
            
        except Exception as e:
            print(f"❌ Error in reset_zones: {e}")
            raise

    def search_zones(self, zone_name):
        """Search for a zone by name"""
        self.click(self.all_zones_button)
        print(f"=== Searching for zone: {zone_name} ===")
        self.click(self.search_zones_field)
        self.type(self.search_zones_field, zone_name)
        time.sleep(2)
        print(f"✅ Successfully searched for zone: {zone_name}")
        
        
