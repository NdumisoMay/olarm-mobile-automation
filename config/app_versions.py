import os

# Base directory for app files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANDROID_APPS_DIR = os.path.join(PROJECT_ROOT, "android", "app")

# App version configurations
APP_VERSIONS = {
    "1.6.6": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-release-166-classic-tokens.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "166",
        "version_name": "1.6.6",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 1.6.6 - Classic tokens version (upgrades to app-release.apk)"
    },
    "1.6.6-oauth": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-release-166-oauth.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "166",
        "version_name": "1.6.6",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 1.6.6 - OAuth version (upgrades to app-release.apk)"
    },
    "2.0.5": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-v2.0.5.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "205",
        "version_name": "2.0.5",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.5 - Base version (upgrades to app-release.apk)"
    },
    "2.0.6": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-v2.0.6.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "206",
        "version_name": "2.0.6",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.6 - Intermediate version (upgrades to app-release.apk)"
    },
    "2.0.7": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-v2.0.7.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "207",
        "version_name": "2.0.7",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.7 - Pre-latest version (upgrades to app-release.apk)"
    },
    "2.0.8": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-v2.0.8.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "208",
        "version_name": "2.0.8",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.8 - Intermediate version (upgrades to app-release.apk)"
    },
    "2.0.9": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-v2.0.9.apk"),
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "209",
        "version_name": "2.0.9",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.9 - Intermediate version (upgrades to app-release.apk)"
    },
    "2.0.10": {
        "apk_path": os.path.join(ANDROID_APPS_DIR, "app-release.apk"),  # Latest version
        "package_name": "com.olarm.olarm1",
        "activity_name": "com.olarm.olarm1.MainActivity",
        "version_code": "210",
        "version_name": "2.0.10",
        "min_sdk": "21",
        "target_sdk": "33",
        "description": "Version 2.0.10 - Latest version (app-release.apk) (target for upgrades)"
    },

}

# Upgrade test scenarios
UPGRADE_SCENARIOS = [
    {
        "name": "upgrade_205_to_app_release",
        
        "from_version": "2.0.5",
        "to_version": "2.0.10",
        "description": "Upgrade from version 2.0.5 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_206_to_app_release",
        "from_version": "2.0.6",
        "to_version": "2.0.10",
        "description": "Upgrade from version 2.0.6 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_207_to_app_release",
        "from_version": "2.0.7",
        "to_version": "2.0.10",
        "description": "Upgrade from version 2.0.7 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_208_to_app_release",
        "from_version": "2.0.8",
        "to_version": "2.0.10",
        "description": "Upgrade from version 2.0.8 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_166_to_app_release",
        "from_version": "1.6.6",
        "to_version": "2.0.10",
        "description": "Upgrade from version 1.6.6 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_166_oauth_to_app_release",
        "from_version": "1.6.6-oauth",
        "to_version": "2.0.10",
        "description": "Upgrade from version 1.6.6-oauth to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    },
    {
        "name": "upgrade_209_to_app_release",
        "from_version": "2.0.9",
        "to_version": "2.0.10",
        "description": "Upgrade from version 2.0.9 to 2.0.10 (app-release.apk)",
        "expected_behavior": "User should remain logged in and see My Devices screen"
    }
]

# Clean installation scenarios (no previous login)
CLEAN_INSTALL_SCENARIOS = [
    {
        "name": "clean_install_166_to_app_release",
        "from_version": "1.6.6",
        "to_version": "2.0.10",
        "description": "Clean installation from version 1.6.6 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_166_oauth_to_app_release",
        "from_version": "1.6.6-oauth",
        "to_version": "2.0.10",
        "description": "Clean installation from version 1.6.6-oauth to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_205_to_app_release",
        "from_version": "2.0.5",
        "to_version": "2.0.10",
        "description": "Clean installation from version 2.0.5 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_206_to_app_release",
        "from_version": "2.0.6",
        "to_version": "2.0.10",
        "description": "Clean installation from version 2.0.6 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_207_to_app_release",
        "from_version": "2.0.7",
        "to_version": "2.0.10",
        "description": "Clean installation from version 2.0.7 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_208_to_app_release",
        "from_version": "2.0.8",
        "to_version": "2.0.10",
        "description": "Clean installation from version 2.0.8 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    },
    {
        "name": "clean_install_209_to_app_release",
        "from_version": "2.0.9",
        "to_version": "2.0.10",
        "description": "Clean installation from version 2.0.9 to 2.0.10 (app-release.apk)",
        "expected_behavior": "App should show landing screen (not logged in)"
    }
]

def get_version_config(version):
    """
    Get configuration for a specific app version
    
    Args:
        version (str): Version string (e.g., "2.0.5")
        
    Returns:
        dict: Version configuration or None if not found
    """
    return APP_VERSIONS.get(version)

def get_latest_version():
    """
    Get the latest version configuration
    
    Returns:
        dict: Latest version configuration
    """
    return APP_VERSIONS["2.0.10"]

def get_upgrade_scenarios():
    """
    Get all upgrade test scenarios
    
    Returns:
        list: List of upgrade scenarios
    """
    return UPGRADE_SCENARIOS

def get_clean_install_scenarios():
    """
    Get all clean installation test scenarios
    
    Returns:
        list: List of clean installation scenarios
    """
    return CLEAN_INSTALL_SCENARIOS

def verify_apk_exists(version):
    """
    Verify that APK file exists for a given version
    
    Args:
        version (str): Version string
        
    Returns:
        bool: True if APK exists, False otherwise
    """
    config = get_version_config(version)
    if not config:
        return False
    
    return os.path.exists(config["apk_path"])

def get_available_versions():
    """
    Get list of versions that have APK files available
    
    Returns:
        list: List of available version strings
    """
    available_versions = []
    
    for version in APP_VERSIONS.keys():
        if verify_apk_exists(version):
            available_versions.append(version)
    
    return available_versions

def get_missing_apks():
    """
    Get list of versions that are missing APK files
    
    Returns:
        list: List of missing version strings
    """
    missing_versions = []
    
    for version in APP_VERSIONS.keys():
        if not verify_apk_exists(version):
            missing_versions.append(version)
    
    return missing_versions

def print_version_status():
    """
    Print status of all app versions and their APK availability
    """
    print("\n📱 App Version Status:")
    print("=" * 50)
    
    for version, config in APP_VERSIONS.items():
        apk_exists = verify_apk_exists(version)
        status = "✅ Available" if apk_exists else "❌ Missing"
        
        print(f"Version {version}: {status}")
        print(f"  Path: {config['apk_path']}")
        print(f"  Description: {config['description']}")
        
        print()
    
    available = get_available_versions()
    missing = get_missing_apks()
    
    print(f"📊 Summary:")
    print(f"  Available versions: {len(available)} - {', '.join(available)}")
    print(f"  Missing versions: {len(missing)} - {', '.join(missing)}")
    print()
    
    # Add explanation about app-release.apk
    print("💡 Note: app-release.apk is always the latest version")
    print("   All upgrade tests target version 2.0.10 (app-release.apk) as the latest version.")
    print("   When you have a new APK, simply replace app-release.apk and")
    print("   all tests will automatically use the new version.")
    print()

# Test data for upgrade scenarios
UPGRADE_TEST_DATA = {
    "valid_user": {
        "username": "test@olarm.com",
        "password": "testpassword123"
    },
    "invalid_user": {
        "username": "invalid@test.com",
        "password": "wrongpassword"
    },
    "upgrade_timeout": 60,  # seconds
    "app_load_timeout": 30,  # seconds
    "login_timeout": 15,  # seconds
    "error_check_timeout": 10  # seconds
}

# Error patterns to check during upgrade
ERROR_PATTERNS = [
    "Error",
    "Crash",
    "App has stopped",
    "Unfortunately",
    "Force Close",
    "ANR",
    "Not Responding",
    "Application Error",
    "System Error"
]

# Success indicators after upgrade
SUCCESS_INDICATORS = [
    "My Devices",
    "Login",
    "text-input-outlined"  # Login form elements
]
