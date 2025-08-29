import pytest
import time
import subprocess
import os
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.landing_page import LandingPage
from helpers.common_tests import do_login, first_login_btn
from utils.data_reader import read_test_data
from config.capabilities import device_farm_config


class TestAppUpgrade:
    """Test suite for app version upgrade scenarios"""
    
    # Test data for different app versions
    APP_VERSIONS = {
        "1.6.6": {
            "apk_path": "android/app/app-release-166-classic-tokens.apk",
            "package_name": "com.olarm.olarm1"
        },
        "1.6.6-oauth": {
            "apk_path": "android/app/app-release-166-oauth.apk",
            "package_name": "com.olarm.olarm1"
        },
        "2.0.5": {
            "apk_path": "android/app/app-v2.0.5.apk",
            "package_name": "com.olarm.olarm1"
        },
        "2.0.6": {
            "apk_path": "android/app/app-v2.0.6.apk", 
            "package_name": "com.olarm.olarm1"
        },
        "2.0.7": {
            "apk_path": "android/app/app-v2.0.7.apk",
            "package_name": "com.olarm.olarm1"
        },
        "2.0.8": {
            "apk_path": "android/app/app-v2.0.8.apk",
            "package_name": "com.olarm.olarm1"
        },
        "2.0.9": {
            "apk_path": "android/app/app-release.apk",  # Latest version
            "package_name": "com.olarm.olarm1"
        },

    }
    
    @pytest.fixture(scope="function")
    def setup_old_version(self, driver, request):
        """Setup fixture to install old version of the app"""
        old_version = request.param
        app_config = self.APP_VERSIONS[old_version]
        
        # Uninstall existing app if present
        try:
            driver.remove_app(app_config["package_name"])
            print(f"✅ Uninstalled existing app version")
        except Exception as e:
            print(f"ℹ️ No existing app to uninstall: {e}")
        
        # Install old version
        apk_path = os.path.join(os.getcwd(), app_config["apk_path"])
        if os.path.exists(apk_path):
            driver.install_app(apk_path)
            print(f"✅ Installed app version {old_version}")
        else:
            pytest.skip(f"APK file not found: {apk_path}")
        
        yield driver, old_version
        
        # Cleanup: uninstall app after test
        try:
            driver.remove_app(app_config["package_name"])
            print(f"✅ Cleaned up app version {old_version}")
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
    
    @pytest.fixture(scope="function") 
    def setup_latest_version(self, driver):
        """Setup fixture to install latest version of the app"""
        latest_config = self.APP_VERSIONS["2.0.9"]
        
        # Install latest version
        apk_path = os.path.join(os.getcwd(), latest_config["apk_path"])
        if os.path.exists(apk_path):
            driver.install_app(apk_path)
            print(f"✅ Installed latest app version (2.0.9 - app-release.apk)")
        else:
            pytest.skip(f"Latest APK file not found: {apk_path}")
        
        yield driver
        
        # Cleanup
        try:
            driver.remove_app(latest_config["package_name"])
            print(f"✅ Cleaned up latest app version")
        except Exception as e:
            print(f"⚠️ Error during cleanup: {e}")
    
    def verify_user_logged_in(self, driver):
        """Verify user is logged in by checking for 'My Devices' screen"""
        try:
            # Wait for app to load
            time.sleep(1.5)
            
            # Check if "My Devices" text is visible
            my_devices_element = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().text("My Devices")'
            )
            
            assert my_devices_element.is_displayed(), "❌ 'My Devices' screen not visible after upgrade"
            print("✅ User remains logged in after upgrade - 'My Devices' screen visible")
            return True
            
        except Exception as e:
            print(f"❌ Failed to verify user login status: {e}")
            return False
    
    def verify_no_errors_during_upgrade(self, driver):
        """Verify no error dialogs or crash dialogs are present"""
        try:
            # Check for common error dialogs
            error_selectors = [
                'new UiSelector().text("Error")',
                'new UiSelector().text("Crash")',
                'new UiSelector().text("App has stopped")',
                'new UiSelector().text("Unfortunately")',
                'new UiSelector().text("Force Close")'
            ]
            
            for selector in error_selectors:
                try:
                    error_element = driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR, 
                        selector
                    )
                    if error_element.is_displayed():
                        pytest.fail(f"❌ Error dialog found: {selector}")
                except:
                    # Element not found, which is good
                    pass
            
            print("✅ No error dialogs detected during upgrade")
            return True
            
        except Exception as e:
            print(f"❌ Error checking for error dialogs: {e}")
            return False
    
    # Note: test_upgrade_from_205_to_app_release removed to avoid duplication
    # This test is now covered by test_upgrade_scenario_205_to_app_release_inplace in test_upgrade_automation.py
    
    # Note: test_upgrade_from_206_to_app_release removed to avoid duplication
    # This test is now covered by test_upgrade_scenario_206_to_app_release_inplace in test_upgrade_automation.py
    
    # Note: test_upgrade_from_207_to_app_release removed to avoid duplication
    # This test is now covered by test_upgrade_scenario_207_to_app_release_inplace in test_upgrade_automation.py
    
    # Note: test_upgrade_from_208_to_app_release removed to avoid duplication
    # This test is now covered by test_upgrade_scenario_208_to_app_release_inplace in test_upgrade_automation.py
    
    def test_upgrade_with_multiple_devices(self, driver):
        """
        Test upgrade scenario with multiple devices to ensure data persistence
        """
        print("\n🔄 Testing upgrade with multiple devices scenario")
        
        # This test would require additional setup for multiple devices
        # For now, we'll create a placeholder test
        pytest.skip("Multiple devices upgrade test requires additional setup")
    
    def test_upgrade_with_network_interruption(self, driver):
        """
        Test upgrade scenario with network interruption during upgrade
        """
        print("\n🔄 Testing upgrade with network interruption")
        
        # This test would simulate network interruption during upgrade
        # For now, we'll create a placeholder test
        pytest.skip("Network interruption upgrade test requires additional setup")
    
    @pytest.mark.parametrize("setup_old_version", ["1.6.6", "1.6.6-oauth", "2.0.5", "2.0.6", "2.0.7", "2.0.8"], indirect=True)
    def test_upgrade_clean_installation(self, setup_old_version, setup_latest_version):
        """
        Test clean installation (no previous login) upgrade scenarios
        """
        driver, old_version = setup_old_version
        
        print(f"\n🔄 Testing clean installation upgrade from {old_version} to 2.0.9 (app-release.apk)")
        
        # Install latest version without logging in first
        try:
            driver.remove_app(self.APP_VERSIONS[old_version]["package_name"])
            print(f"✅ Uninstalled version {old_version}")
            
            latest_config = self.APP_VERSIONS["2.0.9"]
            apk_path = os.path.join(os.getcwd(), latest_config["apk_path"])
            driver.install_app(apk_path)
            print("✅ Installed latest version (2.0.9 - app-release.apk)")
            
            driver.activate_app(latest_config["package_name"])
            print("✅ Launched upgraded app")
            
            # Verify app launches to landing screen (not logged in)
            time.sleep(1.5)
            from helpers.upgrade_helpers import UpgradeHelpers
            upgrade_helper = UpgradeHelpers(driver)
            assert upgrade_helper.verify_landing_screen(), "❌ App should show landing screen for clean install"
            print("✅ Clean installation shows landing screen correctly")
            
        except Exception as e:
            pytest.fail(f"❌ Failed clean installation upgrade: {e}")
    
    def test_upgrade_performance(self, driver):
        """
        Test upgrade performance and timing
        """
        print("\n🔄 Testing upgrade performance")
        
        # This test would measure upgrade time and performance metrics
        # For now, we'll create a placeholder test
        pytest.skip("Performance test requires additional metrics collection setup")
