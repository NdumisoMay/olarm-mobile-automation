import pytest
from drivers.driver_factory import init_driver
from appium.webdriver.appium_service import AppiumService
import requests
import time
from config.capabilities import device_farm_config
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment variables from .env file
load_dotenv()

appium_service = AppiumService()

def pytest_addoption(parser):
    parser.addoption("--device-farm", action="store_true", default=False,
                    help="Run tests on device farm")
    parser.addoption("--platform", type=str, default="android",
                    help="Platform to run tests on (android or ios)")
    parser.addoption("--device-id", action="store", default=None,
                    help="Device farm device ID or name")

def wait_for_appium(timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            res = requests.get("http://localhost:4725/wd/hub/status")
            if res.status_code == 200:
                print("✅ Appium server is live")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    raise RuntimeError("❌ Appium server failed to start within timeout")

def check_device_farm_server():
    """Check if device farm server is accessible"""
    # Parse the server URL to get base URL
    parsed_url = urllib.parse.urlparse(device_farm_config["server_url"])
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    
    try:
        # Try status endpoint
        status_url = f"{base_url}/status"
        print(f"Checking device farm server at: {status_url}")
        res = requests.get(status_url, timeout=10)
        if res.status_code == 200:
            print("✅ Device farm server is accessible")
            return True
            
        print(f"❌ Device farm server returned status code: {res.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to device farm server at {base_url}")
        return False
    except Exception as e:
        print(f"❌ Error checking device farm server: {str(e)}")
        return False

@pytest.fixture(scope="session")
def use_device_farm(request):
    return request.config.getoption("--device-farm")

@pytest.fixture(scope="session")
def platform(request):
    platform = request.config.getoption("--platform").lower()
    if platform not in ["android", "ios"]:
        raise ValueError("Platform must be either 'android' or 'ios'")
    return platform

@pytest.fixture(scope="session")
def device_id(request):
    return request.config.getoption("--device-id")

@pytest.fixture(scope="session", autouse=True)
def start_appium(use_device_farm):
    if not use_device_farm:
        # Only start local Appium server for local testing
        # Force stop any existing Appium service
        try:
            appium_service.stop()
        except:
            pass
        
        # Kill any existing processes on port 4725
        import subprocess
        try:
            subprocess.run(['pkill', '-f', 'appium.*4725'], capture_output=True)
            import time
            time.sleep(2)
        except:
            pass

        # Configure Appium service with custom port and base path
        appium_service.start(args=['--port', '4725', '--base-path', '/wd/hub', '--log', 'appium.log'])
        
        # Wait for Appium server to be ready
        wait_for_appium()

    yield

    if not use_device_farm and appium_service.is_running:
        appium_service.stop()
        print("🧹 Appium service stopped")

@pytest.fixture(scope="function")
def driver(start_appium, use_device_farm, platform, device_id):
    driver = None
    try:
        # Initialize driver with device farm configuration if specified
        driver = init_driver(
            use_device_farm=use_device_farm,
            platform=platform,
            device_id=device_id
        )
        print(f"{'Device Farm' if use_device_farm else 'Local'} {platform} driver initialized successfully")
        
        yield driver
    except Exception as e:
        print(f"❌ Failed to initialize driver: {str(e)}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
                print("🧹 Driver cleaned up successfully")
            except Exception as e:
                print(f"[WARNING] Error during driver cleanup: {e}")

@pytest.fixture(scope="session")
def session_driver(start_appium, use_device_farm, platform, device_id):
    """Session-scoped driver that persists across multiple tests"""
    driver = None
    try:
        # Initialize driver with device farm configuration if specified
        driver = init_driver(
            use_device_farm=use_device_farm,
            platform=platform,
            device_id=device_id
        )
        print(f"{'Device Farm' if use_device_farm else 'Local'} {platform} session driver initialized successfully")
        
        yield driver
    except Exception as e:
        print(f"❌ Failed to initialize session driver: {str(e)}")
        raise
    finally:
        if driver:
            try:
                driver.quit()
                print("🧹 Session driver cleaned up successfully")
            except Exception as e:
                print(f"[WARNING] Error during session driver cleanup: {e}")

@pytest.fixture
def driver_with_uninstall(start_appium, use_device_farm, platform, device_id):
    driver = None
    try:
        driver = init_driver(
            use_device_farm=use_device_farm,
            platform=platform,
            device_id=device_id
        )
        print(f"{'Device Farm' if use_device_farm else 'Local'} {platform} driver initialized successfully")
        
        yield driver
    except Exception as e:
        print(f"❌ Failed to initialize driver: {str(e)}")
        raise
    finally:
        if driver:
            try:
                app_package = device_farm_config["app_package"]
                driver.terminate_app(app_package)
                driver.remove_app(app_package)
                driver.quit()
                print("🧹 Driver and app cleaned up successfully")
            except Exception as e:
                print(f"[WARNING] Error during driver cleanup: {e}")