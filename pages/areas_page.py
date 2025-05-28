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

    area1_label = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().text("Front Door")')
    status = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Armed")')
    status_disarmed = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Disarmed")')
    timestamp = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text(" • Now")')

    from appium.webdriver.common.appiumby import AppiumBy

    def get_area_info_by_label(self, label_text):
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

        # Check each text element for matching content
        for element in text_elements:
            text = element.text.strip()
            if text.lower() in ["armed", "disarmed"]:
                status = text
            elif "now" in text.lower():
                timestamp = text

        if not status:
            raise Exception(f"Status not found for label '{label_text}'")
        if not timestamp:
            raise Exception(f"Timestamp not found for label '{label_text}'")

        return {
            "label": label_text,
            "status": status,
            "time": timestamp
        }

    arm_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("icon-button").instance(4)')

    activity = (AppiumBy.ACCESSIBILITY_ID,'Activity')

    def get_area_container_by_label(self, label_text):
        return self.driver.find_element(
            AppiumBy.XPATH,
            f'//android.widget.TextView[@text="{label_text}"]/parent::android.view.ViewGroup'
        )

    def arm_panel(self):
        self.click(self.arm_button)
        time.sleep(5)

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
        time.sleep(5)

    def is_panel_disarmed(self):
        try:
            return self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Disarmed")')
).text
        except:
            return ""