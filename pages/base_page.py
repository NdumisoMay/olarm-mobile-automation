import os
import time
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver


    def click(self, locator, timeout=10):
        """Wait and click using normal click, fallback to W3C tap if click fails."""
        try:
            element = self.wait_until_clickable(locator, timeout)

            if element.is_displayed() and element.is_enabled():
                print(f"Clicking on: {locator}")
                element.click()
                time.sleep(1)  # Let the app respond
            else:
                raise Exception("Element is not interactable")

        except Exception as e:
            print(f"[Standard click failed] Trying W3C fallback tap on {locator}")
            try:
                element = self.driver.find_element(*locator)
                rect = element.rect
                x = rect['x'] + rect['width'] // 2
                y = rect['y'] + rect['height'] // 2

                finger = PointerInput("touch", "finger")
                action = ActionBuilder(self.driver, mouse=finger)
                action.pointer_action.move_to_location(x, y)
                action.pointer_action.pointer_down()
                action.pointer_action.pointer_up()
                action.perform()
                time.sleep(1)
            except Exception as tap_error:
                self._log_error(locator, "click", tap_error)
                raise

    def type(self, locator, text, timeout=10):
        """Type text into an input field identified by the locator."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.send_keys(text)
        except Exception as e:
            self.driver.save_screenshot("type_error.png")
            print(f"Failed to type on {locator}. Reason: {e}")
            raise  # <- This ensures the test actually fails

    def is_visible(self, locator, timeout=10):
        """Return True if the element is visible within the timeout."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except Exception as e:
            self._log_error(locator, "is_visible", e)
            return False

    def wait_until_clickable(self, locator, timeout=10):
        """Wait until an element becomes clickable and return it."""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_and_click(self, locator, timeout=10):
        """Wait for an element to be clickable and then click it."""
        self.click(locator, timeout)

    def get_text(self, locator, timeout=5):
        """Wait for visibility and get text from the element."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text
        except Exception as e:
            self._log_error(locator, "get_text", e)
            return ""

    def scroll_to_description(self, description):
        """Scroll into view by content description."""
        try:
            return self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().description("{description}"))'
            )
        except Exception as e:
            print(f" Could not scroll to description '{description}': {e}")
            return None

    def _log_error(self, locator, action, error):
        """Helper to log and screenshot on errors."""
        screenshot_path = os.path.join(os.getcwd(), f"{action}_error.png")
        self.driver.save_screenshot(screenshot_path)
        print(f" Failed to {action} on {locator}. Screenshot saved to {screenshot_path}. Reason: {error}")
        traceback.print_exc()
