import time
from socket import send_fds

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class AreasPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    area1_label = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Area 1")')
    status = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Armed")')
    status_disarmed = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Disarmed")')
    timestamp = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" • Now")')
    stay_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(5)')
    sleep_arm_btn = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(6)')


    def get_area_info_by_label(self, label_text, timeout=5):
        # Locate the parent container for the area
        area_container = self.driver.find_element(
            AppiumBy.XPATH,
            f'//android.widget.TextView[@text="{label_text}"]/parent::android.view.ViewGroup'
        )

        # Collect all text elements in the container
        text_elements = area_container.find_elements(
            AppiumBy.XPATH,
            './/android.widget.TextView'
        )

        # Initialize fallback values
        status = None
        timestamp = None
        all_texts = []

        # Check each text element for matching content
        for element in text_elements:
            text = element.text.strip()
            all_texts.append(text)  # For debugging
            
            if text.lower() in ["armed","stay armed","sleep armed", "disarmed"]:
                status = text
            elif "now" in text.lower() or "•" in text or ":" in text:
                timestamp = text

        print(f"DEBUG: All texts found for {label_text}: {all_texts}")
        print(f"DEBUG: Status found: {status}, Timestamp found: {timestamp}")

        if not status:
            raise Exception(f"Status not found for label '{label_text}'. Found texts: {all_texts}")
        if not timestamp:
            # If no timestamp found, use a default
            print(f"WARNING: No timestamp found for {label_text}, using 'Now' as default")
            timestamp = "Now"

        return {
            "label": label_text,
            "status": status,
            "time": timestamp
        }

    arm_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(4)')

    #activity = (AppiumBy.ACCESSIBILITY_ID,'Activity')

    def get_area_container_by_label(self, label_text):
        return self.driver.find_element(
            AppiumBy.XPATH,
            f'//android.widget.TextView[@text="{label_text}"]/parent::android.view.ViewGroup'
        )

    def arm_panel(self):
        self.click(self.arm_button)
        time.sleep(3)

    def is_panel_armed(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Armed")')
).text
        except:
            return ""

    disarm_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(3)')
    def disarm_panel(self):
        self.click(self.disarm_button)
        time.sleep(3)

    def is_panel_disarmed(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Disarmed")')
).text
        except:
            return ""


    #------------------

    def stay_arm(self):
        self.click(self.stay_btn)
        time.sleep(3)

    def is_panel_stay_armed(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Stay Armed")')
                                            ).text
        except:
            return ""

    def sleep_arm(self):
        self.click(self.sleep_arm_btn)
        time.sleep(3)

    def is_panel_sleep_armed(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(6)')
                                            ).text
        except:
            return ""