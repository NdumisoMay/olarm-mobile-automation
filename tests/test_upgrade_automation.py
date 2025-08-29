import pytest
import time
import os
from appium.webdriver.common.appiumby import AppiumBy
from helpers.upgrade_helpers import UpgradeHelpers
from helpers.common_tests import do_login, first_login_btn, do_login_with_classic_tokens
from config.app_versions import (
    get_version_config, 
    get_upgrade_scenarios, 
    get_clean_install_scenarios,
    verify_apk_exists,
    print_version_status,
    UPGRADE_TEST_DATA
)
from pages.landing_page import LandingPage


class TestUpgradeAutomation:
    """Comprehensive upgrade automation test suite for in-place upgrades"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_test_environment(self):
        """Setup test environment and print version status"""
        print("\n" + "="*60)
        print("🚀 UPGRADE AUTOMATION TEST SUITE")
        print("="*60)
        print_version_status()
        print("="*60)
    
    @pytest.fixture(scope="function")
    def upgrade_helper(self, driver):
        """Create upgrade helper instance"""
        return UpgradeHelpers(driver)
    


    def test_upgrade_scenario_166_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test upgrade from version 1.6.6 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 1.6.6 (app-release-166-classic-tokens.apk)
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """
        from_version = "1.6.6"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 1.6.6 (clean installation to start fresh)
        print("Step 1: Installing version 1.6.6...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        # Navigate to login and perform login
        #first_login_btn(driver)
        do_login_with_classic_tokens(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled) - CUSTOM FOR 1.6.6
        print("Step 2.6: Verifying login for version 1.6.6 (classic tokens)...")
        
        # For version 1.6.6, look for "Devices" text instead of "My Devices"
        try:
            # Look for "Devices" text (title of the screen) - this confirms successful login
            devices_element = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().text("Devices")'
            )
            assert devices_element.is_displayed(), "'Devices' screen not visible after login"
            print("✅ Found 'Devices' screen title")
            
            print(f"✅ Successfully logged into version {from_version} (classic tokens)")
            
        except Exception as e:
            print(f"❌ Login verification failed for version {from_version}: {e}")
            # Take a screenshot for debugging
            upgrade_helper.take_screenshot("166_login_failure_debug.png")
            raise AssertionError(f"Failed to login to version {from_version} - classic tokens verification failed")
        
        # For version 1.6.6, we don't verify "My Devices" screen content since it's different
        print("Step 2.7: Skipping My Devices screen content verification for classic tokens version")
        
        # Open drawer menu and verify version 1.6.6 before upgrade
        print("Step 2.8: Verifying version 1.6.6 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("1.6.6", "166_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        # Launch the upgraded app
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "166_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("166_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_scenario_166_oauth_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test in-place upgrade from version 1.6.6-oauth to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 1.6.6-oauth (app-release-166-oauth.apk)
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """
        from_version = "1.6.6-oauth"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 1.6.6-oauth (clean installation to start fresh)
        print("Step 1: Installing version 1.6.6-oauth...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        # Navigate to login and perform login
        #first_login_btn(driver)
        do_login_with_classic_tokens(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled) - CUSTOM FOR 1.6.6-OAUTH
        print("Step 2.6: Verifying login for version 1.6.6-oauth...")
        
        # For version 1.6.6-oauth, look for "Devices" text instead of "My Devices"
        try:
            # Look for "Devices" text (title of the screen) - this confirms successful login
            devices_element = driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 
                'new UiSelector().text("Devices")'
            )
            assert devices_element.is_displayed(), "'Devices' screen not visible after login"
            print("✅ Found 'Devices' screen title")
            
            print(f"✅ Successfully logged into version {from_version} (OAuth)")
            
        except Exception as e:
            print(f"❌ Login verification failed for version {from_version}: {e}")
            # Take a screenshot for debugging
            upgrade_helper.take_screenshot("166_oauth_login_failure_debug.png")
            raise AssertionError(f"Failed to login to version {from_version} - OAuth verification failed")
        
        # For version 1.6.6-oauth, we don't verify "My Devices" screen content since it's different
        print("Step 2.7: Skipping My Devices screen content verification for OAuth version")
        
        # Open drawer menu and verify version 1.6.6-oauth before upgrade
        print("Step 2.8: Verifying version 1.6.6-oauth in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("1.6.6", "166_oauth_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        # Launch the upgraded app
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "166_oauth_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("166_oauth_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_scenario_205_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test in-place upgrade from version 2.0.5 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 2.0.5
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """
        from_version = "2.0.5"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 2.0.5 (clean installation to start fresh)
        print("Step 1: Installing version 2.0.5...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        # Navigate to login and perform login
        first_login_btn(driver)
        do_login(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled)
        assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
        print(f"✅ Successfully logged into version {from_version}")
        
        # Verify My Devices screen contains expected functional content before upgrade
        assert upgrade_helper.verify_my_devices_screen_content(), f"My Devices screen does not contain expected functional content in version {from_version}"
        
        # Open drawer menu and verify version 2.0.5 before upgrade
        print("Step 2.6: Verifying version 2.0.5 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.5", "205_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        # Launch the upgraded app
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "205_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("205_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_scenario_206_to_app_release_inplace(self, driver, upgrade_helper):
        """
         Test in-place upgrade from version 2.0.6 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 2.0.6
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """
       
        from_version = "2.0.6"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 2.0.6 (clean installation to start fresh)
        print("Step 1: Installing version 2.0.6...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        first_login_btn(driver)
        do_login(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled)
        assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
        print(f"✅ Successfully logged into version {from_version}")
        
        # Verify My Devices screen contains expected functional content before upgrade
        assert upgrade_helper.verify_my_devices_screen_content(), f"My Devices screen does not contain expected functional content in version {from_version}"
        
        # Open drawer menu and verify version 2.0.6 before upgrade
        print("Step 2.6: Verifying version 2.0.6 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.6", "206_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "206_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("206_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_scenario_207_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test upgrade from version 2.0.7 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 2.0.7
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        """
        from_version = "2.0.7"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 2.0.7 (clean installation to start fresh)
        print("Step 1: Installing version 2.0.7...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        first_login_btn(driver)
        do_login(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled)
        assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
        print(f"✅ Successfully logged into version {from_version}")
        
        # Verify My Devices screen contains expected functional content before upgrade
        assert upgrade_helper.verify_my_devices_screen_content(), f"My Devices screen does not contain expected functional content in version {from_version}"
        
        # Open drawer menu and verify version 2.0.7 before upgrade
        print("Step 2.6: Verifying version 2.0.7 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.7", "207_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "207_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("207_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_performance_metrics_inplace(self, driver, upgrade_helper):
        """
        Test upgrade performance and timing metrics across multiple scenarios
        """
        print(f"\n🔄 Testing in-place upgrade performance metrics")
        
        # Test multiple upgrade scenarios for performance comparison
        # Note: 1.6.6 versions are tested separately due to different login flows
        test_scenarios = [
            ("2.0.5", "2.0.10"),
            ("2.0.6", "2.0.10"),
            ("2.0.7", "2.0.10"),
            ("2.0.8", "2.0.10"),
            ("2.0.9", "2.0.10")
        ]
        
        performance_results = {}
        
        for from_version, to_version in test_scenarios:
            print(f"\n📊 Testing performance: {from_version} → {to_version}")
            
            # Check if APK files exist
            if not verify_apk_exists(from_version):
                print(f"⚠️ Skipping {from_version} - APK not found")
                continue
            if not verify_apk_exists(to_version):
                print(f"⚠️ Skipping {to_version} - APK not found")
                continue
            
            # Record start time
            start_time = time.time()
            
            # Step 1: Install and login to old version
            old_config = get_version_config(from_version)
            install_start = time.time()
            assert upgrade_helper.install_app_version_clean(
                old_config["apk_path"], 
                old_config["package_name"]
            ), f"Failed to install version {from_version}"
            install_time = time.time() - install_start
            
            launch_start = time.time()
            assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
            launch_time = time.time() - launch_start
            
            login_start = time.time()
            
            # For newer versions (2.0.5+), use the standard login flow
            first_login_btn(driver)
            do_login(driver)
            assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
                
            login_time = time.time() - login_start
            
            # Step 2: In-place upgrade to latest version
            upgrade_start = time.time()
            new_config = get_version_config(to_version)
            
            # Install new version over existing one (in-place upgrade)
            assert upgrade_helper.install_app_version(
                new_config["apk_path"], 
                new_config["package_name"]
            ), f"Failed to install version {to_version}"
            
            assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
            upgrade_time = time.time() - upgrade_start
            
            # Step 3: Verify upgrade results
            verify_start = time.time()
            assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
            assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
            verify_time = time.time() - verify_start
            
            total_time = time.time() - start_time
            
            # Store performance metrics
            performance_results[f"{from_version}→{to_version}"] = {
                "install_time": install_time,
                "launch_time": launch_time,
                "login_time": login_time,
                "upgrade_time": upgrade_time,
                "verify_time": verify_time,
                "total_time": total_time
            }
            
            # Cleanup for next test
            driver.remove_app(new_config["package_name"])
        
        # Print comprehensive performance metrics
        print(f"\n📊 Comprehensive Performance Metrics:")
        print("=" * 80)
        for scenario, metrics in performance_results.items():
            print(f"\n{scenario}:")
            print(f"  Install time: {metrics['install_time']:.2f}s")
            print(f"  Launch time: {metrics['launch_time']:.2f}s")
            print(f"  Login time: {metrics['login_time']:.2f}s")
            print(f"  Upgrade time: {metrics['upgrade_time']:.2f}s")
            print(f"  Verification time: {metrics['verify_time']:.2f}s")
            print(f"  Total time: {metrics['total_time']:.2f}s")
        
        # Calculate averages
        if performance_results:
            avg_install = sum(m['install_time'] for m in performance_results.values()) / len(performance_results)
            avg_launch = sum(m['launch_time'] for m in performance_results.values()) / len(performance_results)
            avg_login = sum(m['login_time'] for m in performance_results.values()) / len(performance_results)
            avg_upgrade = sum(m['upgrade_time'] for m in performance_results.values()) / len(performance_results)
            avg_verify = sum(m['verify_time'] for m in performance_results.values()) / len(performance_results)
            avg_total = sum(m['total_time'] for m in performance_results.values()) / len(performance_results)
            
            print(f"\n📈 Average Performance Metrics:")
            print(f"  Average install time: {avg_install:.2f}s")
            print(f"  Average launch time: {avg_launch:.2f}s")
            print(f"  Average login time: {avg_login:.2f}s")
            print(f"  Average upgrade time: {avg_upgrade:.2f}s")
            print(f"  Average verification time: {avg_verify:.2f}s")
            print(f"  Average total time: {avg_total:.2f}s")
        
        # Assert reasonable performance thresholds
        for scenario, metrics in performance_results.items():
            assert metrics['install_time'] < 60, f"Install time too slow for {scenario}: {metrics['install_time']:.2f}s"
            assert metrics['launch_time'] < 30, f"Launch time too slow for {scenario}: {metrics['launch_time']:.2f}s"
            assert metrics['login_time'] < 30, f"Login time too slow for {scenario}: {metrics['login_time']:.2f}s"
            assert metrics['upgrade_time'] < 120, f"Upgrade time too slow for {scenario}: {metrics['upgrade_time']:.2f}s"
            assert metrics['total_time'] < 300, f"Total test time too slow for {scenario}: {metrics['total_time']:.2f}s"
        
        print(f"✅ In-place upgrade performance test completed successfully")
    
    def test_upgrade_scenario_208_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test upgrade from version 2.0.8 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 2.0.8
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """ 
        from_version = "2.0.8"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 2.0.8 (clean installation to start fresh)
        print("Step 1: Installing version 2.0.8...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        # Navigate to login and perform login
        first_login_btn(driver)
        do_login(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled)
        assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
        print(f"✅ Successfully logged into version {from_version}")
        
        # Verify My Devices screen contains expected functional content before upgrade
        assert upgrade_helper.verify_my_devices_screen_content(), f"My Devices screen does not contain expected functional content in version {from_version}"
        
        # Open drawer menu and verify version 2.0.8 before upgrade
        print("Step 2.6: Verifying version 2.0.8 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.8", "208_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        # Launch the upgraded app
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "208_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("208_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_scenario_209_to_app_release_inplace(self, driver, upgrade_helper):
        """
        Test upgrade from version 2.0.9 to 2.0.10 (app-release.apk)
        Steps:
        1. Install version 2.0.9
        2. Login to the app
        3. Upgrade to 2.0.10 (app-release.apk) (without uninstalling)
        4. Verify user remains logged in
        5. Verify "My Devices" screen is visible
        6. Verify no errors during upgrade
        7. Uninstall the app
        """ 
        from_version = "2.0.9"
        to_version = "2.0.10"
        
        print(f"\n🔄 Testing in-place upgrade scenario: {from_version} → {to_version}")
        
        # Check if APK files exist
        if not verify_apk_exists(from_version):
            pytest.skip(f"APK file for version {from_version} not found")
        if not verify_apk_exists(to_version):
            pytest.skip(f"APK file for version {to_version} not found")
        
        # Step 1: Install version 2.0.9 (clean installation to start fresh)
        print("Step 1: Installing version 2.0.9...")
        old_config = get_version_config(from_version)
        assert upgrade_helper.install_app_version_clean(
            old_config["apk_path"], 
            old_config["package_name"]
        ), f"Failed to install version {from_version}"
        
        # Step 2: Launch app and login
        print("Step 2: Launching app and logging in...")
        assert upgrade_helper.launch_app(old_config["package_name"]), "Failed to launch old version"
        
        # Navigate to login and perform login
        first_login_btn(driver)
        do_login(driver)
        
        # Handle notification permission dialog that appears after login (before checking login status)
        print("Step 2.5: Auto-granting all permissions after login...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Now verify login was successful (after permission dialog is handled)
        assert upgrade_helper.verify_user_logged_in(), f"Failed to login to version {from_version}"
        print(f"✅ Successfully logged into version {from_version}")
        
        # Verify My Devices screen contains expected functional content before upgrade
        assert upgrade_helper.verify_my_devices_screen_content(), f"My Devices screen does not contain expected functional content in version {from_version}"
        
        # Open drawer menu and verify version 2.0.9 before upgrade
        print("Step 2.6: Verifying version 2.0.9 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.9", "209_version_before_upgrade.png")
        
        # Step 3: In-place upgrade to 2.0.10 (app-release.apk) (preserving user data)
        print("Step 3: Performing in-place upgrade to 2.0.10 (app-release.apk)...")
        new_config = get_version_config(to_version)
        
        # Install new version over the existing one (in-place upgrade - NO uninstall)
        # This preserves user login state and app data
        assert upgrade_helper.install_app_version_direct(
            new_config["apk_path"], 
            new_config["package_name"]
        ), f"Failed to install version {to_version}"
        
        # Launch the upgraded app
        assert upgrade_helper.launch_app(new_config["package_name"]), "Failed to launch upgraded app"
        
        # Auto-grant all permissions after upgrade (drawer menu becomes visible after this)
        print("Step 3.5: Auto-granting all permissions after upgrade...")
        upgrade_helper.auto_grant_all_permissions()
        
        # Step 4: Verify upgrade results FIRST (before trying drawer menu)
        print("Step 4: Verifying upgrade results...")
        
        assert upgrade_helper.wait_for_app_load(), "App did not load after upgrade"
        assert upgrade_helper.verify_user_logged_in(), "User not logged in after upgrade"
        
        my_devices_element = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, 
            'new UiSelector().text("My Devices")'
        )
        assert my_devices_element.is_displayed(), "'My Devices' screen not visible after upgrade"
        
        # CRITICAL: Verify My Devices screen contains expected functional content and NO error messages
        assert upgrade_helper.verify_my_devices_screen_content(), "My Devices screen does not contain expected functional content after upgrade"
        
        error_messages = upgrade_helper.check_for_error_dialogs()
        assert len(error_messages) == 0, f"Error dialogs found during upgrade: {error_messages}"
        
        # Only try drawer menu verification if the screen content is valid
        print("Step 3.6: Verifying version 2.0.10 in drawer menu...")
        upgrade_helper.open_drawer_menu_and_verify_version("2.0.10", "209_version_after_upgrade.png")
        
        # Take final screenshot showing "My Devices" screen
        upgrade_helper.take_screenshot("209_my_devices_after_upgrade.png")
        
        print(f"✅ In-place upgrade from {from_version} to {to_version} completed successfully")
        
        # Step 5: Uninstall the app
        print("Step 5: Uninstalling the app...")
        driver.remove_app(new_config["package_name"])
        print("✅ App uninstalled successfully")
    
    def test_upgrade_error_handling(self, driver, upgrade_helper):
        """
        Test upgrade error handling and recovery
        """
        print(f"\n🔄 Testing upgrade error handling")
        
        # Test with invalid APK path
        invalid_apk_path = "/invalid/path/app.apk"
        result = upgrade_helper.install_app_version(invalid_apk_path, "com.olarm.olarm1")
        assert not result, "Should fail with invalid APK path"
        
        # Test app launch with non-existent package
        result = upgrade_helper.launch_app("com.nonexistent.app")
        assert not result, "Should fail with non-existent package"
        
        # Test version verification with non-existent package
        result = upgrade_helper.verify_app_installed("com.nonexistent.app")
        assert not result, "Should return False for non-existent package"
        
        print(f"✅ Upgrade error handling test completed successfully")
    
    @pytest.mark.skip(reason="Requires multiple devices setup")
    def test_upgrade_multiple_devices(self, driver, upgrade_helper):
        """
        Test upgrade scenario with multiple devices
        """
        print(f"\n🔄 Testing upgrade with multiple devices")
        pytest.skip("Multiple devices upgrade test requires additional setup")
    
    @pytest.mark.skip(reason="Requires network simulation setup")
    def test_upgrade_network_interruption(self, driver, upgrade_helper):
        """
        Test upgrade scenario with network interruption
        """
        print(f"\n🔄 Testing upgrade with network interruption")
        pytest.skip("Network interruption upgrade test requires additional setup")
