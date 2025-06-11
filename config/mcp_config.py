"""
MCP (Mobile Cloud Platform) configuration settings
"""

MCP_CONFIG = {
    'platformName': 'Android',
    'appium:automationName': 'UiAutomator2',
    'appium:deviceName': 'Samsung Galaxy S21',  # This will be overridden by MCP
    'appium:app': 'path/to/your/app.apk',  # Replace with your app path in MCP
    'appium:noReset': False,
    'appium:fullReset': True,
    'appium:newCommandTimeout': 300,
    'appium:mcp': True,  # Flag to indicate MCP execution
    'appium:mcpDeviceSerialId': None,  # Will be set by MCP
} 