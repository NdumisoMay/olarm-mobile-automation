import pytest
from drivers.driver_factory import init_driver
from appium.webdriver.appium_service import AppiumService
import requests
import time

appium_service = AppiumService()

def wait_for_appium(timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            res = requests.get("http://localhost:4723/status")
            if res.status_code == 200:
                print("✅ Appium server is live")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    raise RuntimeError("❌ Appium server failed to start within timeout")

@pytest.fixture(scope="session", autouse=True)
def start_appium():
    if appium_service.is_running:
        appium_service.stop()

    appium_service.start()
    wait_for_appium()

    yield

    appium_service.stop()
    print("🧹 Appium service stopped")

@pytest.fixture(scope="function")
def driver(start_appium):
    driver = init_driver()  # should use "http://localhost:4723"
    yield driver
    driver.quit()

