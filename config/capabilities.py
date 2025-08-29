import os
import socket

def get_local_ip():
    try:
        # Try to get the Wi-Fi interface IP
        cmd = "networksetup -getinfo Wi-Fi | grep 'IP address' | awk '{print $3}'"
        return os.popen(cmd).read().strip()
    except:
        return None

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# App paths for both platforms
android_app = os.path.abspath(os.path.join(project_root, "android", "app", "app-release.apk"))
ios_app = os.getenv("IOS_APP_PATH", "")

# Android capabilities for local testing
android_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",
    # Removed "app" to prevent automatic installation during driver creation
    "appPackage": "com.olarm.olarm1",
    "appActivity": "com.olarm.olarm1.MainActivity",
    "noReset": True,  # Changed to True to prevent unnecessary resets
    "fullReset": False,  # Changed to False to prevent full reset during initialization
    "autoLaunch": False,  # Added to prevent auto-launch during initialization
    "autoGrantPermissions": True,  # Changed back to True to prevent permission dialogs
    "newCommandTimeout": 300,
    "adbExecTimeout": 60000,
    "uiautomator2ServerLaunchTimeout": 60000,
    "uiautomator2ServerInstallTimeout": 60000
}

# Base capabilities for each platform
android_base_caps = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "appWaitActivity": "*",
    "appWaitForLaunch": True,
    "autoLaunch": False,  # Changed to False to prevent auto-launch during initialization
    "autoGrantPermissions": True,  # Changed back to True to prevent permission dialogs
    "noReset": True,  # Changed to True to prevent unnecessary resets
    "fullReset": False,  # Changed to False to prevent full reset during initialization
    "newCommandTimeout": 300,
    # Debug logging
    "printPageSourceOnFindFailure": True,
    "adbExecTimeout": 60000,
    "uiautomator2ServerLaunchTimeout": 60000,
    "uiautomator2ServerInstallTimeout": 60000,
    "remoteAppsCacheLimit": 0,
    "enforceAppInstall": False  # Changed to False to prevent forced install during initialization
}

ios_base_caps = {
    "platformName": "iOS",
    "automationName": "XCUITest",
    "platformVersion": "16.3",
    "appWaitForLaunch": True,
    "autoLaunch": True,
    "autoAcceptAlerts": True,
    "noReset": False,
    "fullReset": True,
    "newCommandTimeout": 300,
    "wdaLocalPort": 8100,
    "useNewWDA": False,
    "showXcodeLog": True,
    "simpleIsVisibleCheck": True,
    # Debug logging
    "printPageSourceOnFindFailure": True,
    "webkitDebugProxyPort": 27753
}

def get_device_farm_caps(platform="android", device_id=None):
    """Get capabilities for a specific platform and device"""
    if platform not in ["android", "ios"]:
        raise ValueError("Platform must be either 'android' or 'ios'")
    
    # Get base capabilities for the platform
    base_caps = android_base_caps if platform == "android" else ios_base_caps
    
    # Start with base capabilities
    caps = base_caps.copy()
    
    # Set app path (removed automatic app installation)
    if platform == "android":
        # Removed "app" to prevent automatic installation during driver creation
        caps["appPackage"] = "com.olarm.olarm1"
        caps["appActivity"] = "com.olarm.olarm1.MainActivity"
    else:
        # Removed "app" to prevent automatic installation during driver creation
        caps["bundleId"] = "com.olarm.olarm1"
    
    # Add device ID if provided
    if device_id:
        caps["udid"] = device_id
        caps["deviceName"] = device_id
    else:
        # Default device names if no specific device requested
        caps["deviceName"] = "Android Device" if platform == "android" else "iOS Device"
    
    # Add common device farm capabilities
    caps.update({
        "networkConnectionTimeout": 60000,
        "commandTimeouts": {
            "default": 60000,
            "getStatus": 60000
        },
        # Debug settings
        "debug": True,
        "systemPort": 8201,
        "clearSystemFiles": True,
        "skipServerInstallation": False
    })
    
    print(f"\nUsing capabilities for {platform}:")
    for key, value in caps.items():
        print(f"{key}: {value}")
    
    return caps

# Network configuration
network_config = {
    "local_ip": get_local_ip(),
    "use_local_network": True if get_local_ip() else False
}

# Device Farm configuration
device_farm_config = {
    "server_url": "http://localhost:4725/wd/hub",
    "app_package": "com.olarm.olarm1",
    "connect_timeout": 60000,
    "command_timeout": 60000,
    "max_retry": 3,
    "retry_delay": 5000
}

# Local test configuration
local_config = {
    "android": {
        **android_base_caps,
        "deviceName": "emulator-5554",
        "app": android_app,
        "appPackage": "com.olarm.olarm1",
        "appActivity": "com.olarm.olarm1.MainActivity"
    },
    "ios": {
        **ios_base_caps,
        "deviceName": "iPhone Simulator",
        "app": ios_app
    }
}

# MCP capabilities
mcp_caps = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:platformVersion": "13.0",  # Can be overridden by device selection
    "appium:deviceName": "Samsung.*",  # Wildcard for Samsung devices
    "appium:app": "storage:filename=olarm_app.apk",  # Format: storage:filename=your_app.apk
    "appium:noReset": False,
    "appium:fullReset": True,
    "appium:autoGrantPermissions": True,
    "appium:newCommandTimeout": 300,
    "appium:appWaitActivity": "*",
    "appium:appWaitForLaunch": True,
    "appium:autoLaunch": True,
    "appium:mcpInstallByName": True,
}

# MCP server configuration
mcp_config = {
    "server_url": "https://appium.bitbar.com/wd/hub",  # Standard MCP server URL
    "app_package": "com.olarm.olarm1",
    "mcp_enabled": True,
    "mcp_api_key": os.getenv("MCP_API_KEY", ""),
    "mcp_project": os.getenv("MCP_PROJECT", "olarm"),
    "mcp_device_groups": ["SAMSUNG", "ANDROID_13"],  # Device group filters
    "mcp_framework": "APPIUM_PYTHON",
    "mcp_timeout": 3600,  # Session timeout in seconds
}
