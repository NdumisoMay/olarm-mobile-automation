from appium import webdriver
from appium.options.common import AppiumOptions
from config.capabilities import get_device_farm_caps, device_farm_config, local_config
import time
import requests
import os
import socket

def wait_for_server(url, timeout=60, interval=5):
    """Wait for server to be available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/status", timeout=5)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(interval)
    return False

def init_driver(use_device_farm=False, platform="android", device_id=None):
    """Initialize WebDriver with appropriate capabilities
    
    Args:
        use_device_farm (bool): Whether to use device farm
        platform (str): Either 'android' or 'ios'
        device_id (str): Device ID or name from device farm
    """
    max_retries = device_farm_config.get("max_retry", 3)
    retry_delay = device_farm_config.get("retry_delay", 5000) / 1000  # Convert to seconds
    driver = None
    
    for attempt in range(max_retries):
        try:
            if use_device_farm:
                print(f"Initializing {platform} device farm driver (Attempt {attempt + 1}/{max_retries})")
                
                # Get capabilities for the specified platform and device
                caps = get_device_farm_caps(platform, device_id)
                
                # Create Appium options
                options = AppiumOptions()
                for cap_name, cap_value in caps.items():
                    options.set_capability(cap_name, cap_value)
                
                server_url = device_farm_config["server_url"]
                
                # If using local network, try to ensure we're using the correct interface
                if device_farm_config.get("network_config", {}).get("use_local_network"):
                    local_ip = device_farm_config["network_config"]["local_ip"]
                    if local_ip:
                        os.environ["CURL_INTERFACE"] = local_ip
                        print(f"Using local network interface: {local_ip}")
                
                # Wait for server to be available
                if not wait_for_server(server_url.split("/wd/hub")[0]):
                    print("Warning: Device farm server not responding to status check")
                
                # Connect to device farm
                driver = webdriver.Remote(
                    command_executor=server_url,
                    options=options
                )
                print(f"✅ Successfully connected to {platform} device farm")
                return driver
            else:
                print(f"Initializing local {platform} driver")
                # Use local configuration
                options = AppiumOptions()
                local_caps = local_config[platform]
                for cap_name, cap_value in local_caps.items():
                    options.set_capability(cap_name, cap_value)
                
                server_url = device_farm_config["server_url"]  # Use the configured server URL
                driver = webdriver.Remote(
                    command_executor=server_url,
                    options=options
                )
                print(f"✅ Successfully connected to local {platform} Appium server")
                return driver
                
        except Exception as e:
            print(f"❌ Driver initialization failed (Attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                raise Exception(f"Failed to initialize driver after {max_retries} attempts: {str(e)}")
    
    return driver  # This line should never be reached due to the raise in the else block above

