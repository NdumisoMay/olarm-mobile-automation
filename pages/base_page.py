import os
import time
import traceback
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import Interaction
from selenium.common.exceptions import NoSuchElementException
import time


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_and_click(self, locator, timeout=5):
        """Wait for an element to be clickable and then click it."""
        try:
            element = self.wait_until_clickable(locator, timeout)
            self.click(locator)
            return element
        except Exception as e:
            self._log_error(locator, "wait_and_click", e)
            raise

    def click(self, locator, timeout=5):
        """Wait and click using normal click, fallback to W3C tap if click fails."""
        try:
            print(f"[Clicking] Trying to click: {locator}")
            element = self.wait_until_clickable(locator, timeout)

            if element.is_displayed() and element.is_enabled():
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
            element.clear()  # Clear existing text
            element.send_keys(text)
            time.sleep(0.5)  # Small wait after typing
        except Exception as e:
            self._log_error(locator, "type", e)
            raise

    def is_visible(self, locator, timeout=10):
        """Return the element if it becomes visible within the timeout, else fail."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception as e:
            self._log_error(locator, "is_visible", e)
            raise

    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except:
            return False

    def wait_until_clickable(self, locator, timeout=5):
        """Wait until an element becomes clickable and return it."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception as e:
            self._log_error(locator, "wait_until_clickable", e)
            raise

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

    def scroll_to_description(self, description, max_swipes=10):
        screen_size = self.driver.get_window_size()
        start_x = screen_size['width'] / 2
        start_y = screen_size['height'] * 0.8
        end_y = screen_size['height'] * 0.2

        for attempt in range(max_swipes):
            try:
                el = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().text("{description}")'
                )
                print(f"✅ Found element with text '{description}' on attempt {attempt + 1}")
                return el
            except NoSuchElementException:
                print(f"🔄 Scrolling attempt {attempt + 1} to find '{description}'")

                finger = PointerInput("touch", "finger")
                actions = ActionBuilder(self.driver)
                actions.pointer_action.move_to_location(int(start_x), int(start_y))
                actions.pointer_action.pointer_down()
                actions.pointer_action.pause(0.2)
                actions.pointer_action.move_to_location(int(start_x), int(end_y))
                actions.pointer_action.release()
                actions.perform()
                time.sleep(1)

        raise AssertionError(f"❌ Could not find element with text '{description}' after {max_swipes} scrolls")

    def _log_error(self, locator, action, error):
        """Helper to log and screenshot on errors."""
        screenshot_path = os.path.join(os.getcwd(), f"{action}_error.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"❌ Failed to {action} on {locator}. Screenshot saved to {screenshot_path}. Error: {str(error)}")
        traceback.print_exc()

#Reset device
