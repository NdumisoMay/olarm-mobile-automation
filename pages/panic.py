import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class PanicPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    # Main panic button to access the Send Panic screen
    panic_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Panic")')
    
    # Send Panic screen title - try multiple variations
    send_panic_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Send Panic")')
    # send_panic_title_alt = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Panic")')
    # send_panic_title_alt2 = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Send")')
    
    # Emergency type label
    emergency_type_label = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Emergency type")')
    
    # Emergency type buttons - using resourceId and instance
    fire_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(1)')
    panic_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(2)')
    medical_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(3)')
    
    
    # Show all emergency contacts button
    show_all_emergency_contacts_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("button")')
    
    # Alternative locator for emergency contacts button
    emergency_contacts_btn = (AppiumBy.ACCESSIBILITY_ID, "Show all emergency contacts")
    
    # Information icon next to "Emergency type"
    emergency_type_info_icon = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("i")')
    
    fire_panic_acivated = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Fire Panic Activated")')   
    panic_acivated = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Panic Activated")')
    medical_panic_acivated = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Medical Panic Activated")')

    emergency_contacts_title = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Emergency contacts")')
    national_emergency  = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("NE, NATIONAL EMERGENCY")')
    saps_police = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("NE, NATIONAL EMERGENCY")')
    er24_ambulance = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("EA, ER24 AMBULANCE")')
    national_crimestop = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("NC, NATIONAL CRIMESTOP")')

    emergency_contacts_back_btn = (AppiumBy.ACCESSIBILITY_ID, 'Back')

    okay_btn_panic_activated = (AppiumBy.ACCESSIBILITY_ID, 'Okay')

    def click_okay_btn_panic_activated(self):
        """Click the Okay button"""
        self.click(self.okay_btn_panic_activated)
        time.sleep(1)

    def click_emergency_contacts_back_btn(self):
        """Click the Back button"""
        self.click(self.emergency_contacts_back_btn)
        time.sleep(1)
    
    def click_panic_button_bottom_nav(self):
        """Click the main panic button to access Send Panic screen"""
        self.click(self.panic_btn)
        time.sleep(1)
    
    def click_fire_emergency(self):
        """Click the Fire emergency button"""
        self.click(self.fire_button)
        time.sleep(0.5)
    
    def click_panic_emergency(self):
        """Click the Panic emergency button"""
        self.click(self.panic_button)
        time.sleep(0.5)
    
    def click_medical_emergency(self):
        """Click the Medical emergency button"""
        self.click(self.medical_button)
        time.sleep(0.5)
    
    def click_show_all_emergency_contacts(self):
        """Click the Show all emergency contacts button"""
        self.click(self.emergency_contacts_btn)
        time.sleep(1)
    
    def is_send_panic_screen_visible(self):
        """Check if the Send Panic screen is visible"""
        try:
            return self.is_visible(self.send_panic_title)
        except:
            try:
                return self.is_visible(self.send_panic_title_alt)
            except:
                try:
                    return self.is_visible(self.send_panic_title_alt2)
                except:
                    return False
    
    def is_emergency_type_label_visible(self):
        """Check if the Emergency type label is visible"""
        return self.is_visible(self.emergency_type_label)
    
    def are_emergency_buttons_visible(self):
        """Check if all emergency buttons are visible"""
        fire_visible = self.is_visible(self.fire_button)
        panic_visible = self.is_visible(self.panic_button)
        medical_visible = self.is_visible(self.medical_button)
        return fire_visible and panic_visible and medical_visible
    
    def is_emergency_contacts_button_visible(self):
        """Check if the Show all emergency contacts button is visible"""
        return self.is_visible(self.show_all_emergency_contacts_btn)
    