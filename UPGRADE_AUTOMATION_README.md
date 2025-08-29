# App Upgrade Automation Framework

This framework provides comprehensive automated testing for app version upgrades using Appium. It ensures that users remain logged in and can access their devices after upgrading from older versions to the latest version.

## Overview

The upgrade automation framework tests the following scenarios:
- Upgrades from version 2.0.5 to 2.0.8
- Upgrades from version 2.0.6 to 2.0.8  
- Upgrades from version 2.0.7 to 2.0.8
- Clean installations (no previous login)
- Performance metrics during upgrades
- Error handling and recovery

## Key Features

✅ **Login Persistence**: Verifies users remain logged in after upgrade  
✅ **Device Access**: Confirms "My Devices" screen is visible after upgrade  
✅ **Error Detection**: Checks for crash dialogs and error messages  
✅ **Performance Metrics**: Measures upgrade timing and performance  
✅ **Screenshot Capture**: Debugging support with automatic screenshots  
✅ **Multiple Scenarios**: Tests various upgrade paths and clean installations  

## Project Structure

```
olarm-mobile-automation/
├── tests/
│   ├── test_app_upgrade.py          # Original upgrade tests
│   └── test_upgrade_automation.py   # Streamlined upgrade tests
├── helpers/
│   └── upgrade_helpers.py           # Upgrade-specific helper functions
├── config/
│   └── app_versions.py              # Version configuration and management
└── android/app/
    ├── app-v2.0.5.apk              # Version 2.0.5 APK
    ├── app-v2.0.6.apk              # Version 2.0.6 APK
    ├── app-v2.0.7.apk              # Version 2.0.7 APK
    └── app-release.apk             # Latest version 2.0.8 APK
```

## Prerequisites

1. **APK Files**: Place the required APK files in `android/app/` directory:
   - `app-v2.0.5.apk`
   - `app-v2.0.6.apk` 
   - `app-v2.0.7.apk`
   - `app-release.apk` (latest version)

2. **Appium Server**: Ensure Appium server is running (will be started automatically)

3. **Android Device/Emulator**: Connected Android device or running emulator

4. **Python Dependencies**: Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### App Versions Configuration

The `config/app_versions.py` file manages all version configurations:

```python
APP_VERSIONS = {
    "2.0.5": {
        "apk_path": "android/app/app-v2.0.5.apk",
        "package_name": "com.olarm.olarm1",
        "version_name": "2.0.5"
    },
    # ... other versions
}
```

### Test Data

Test credentials and configuration are managed in the same file:

```python
UPGRADE_TEST_DATA = {
    "valid_user": {
        "username": "primary@olarm.local",
        "password": "DiasLunch@1pm"
    },
    "upgrade_timeout": 60,
    "app_load_timeout": 30
}
```

## Running Tests

### Run All Upgrade Tests

```bash
python -m pytest tests/test_upgrade_automation.py -v
```

### Run Specific Upgrade Scenario

```bash
# Test upgrade from 2.0.5 to 2.0.8
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_upgrade_scenario_205_to_208 -v

# Test upgrade from 2.0.6 to 2.0.8
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_upgrade_scenario_206_to_208 -v

# Test upgrade from 2.0.7 to 2.0.8
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_upgrade_scenario_207_to_208 -v
```

### Run Clean Installation Tests

```bash
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_clean_installation_scenarios -v
```

### Run Performance Tests

```bash
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_upgrade_performance_metrics -v
```

### Run with Screenshots

```bash
python -m pytest tests/test_upgrade_automation.py -v --screenshot
```

### Run with HTML Report

```bash
python -m pytest tests/test_upgrade_automation.py -v --html=reports/upgrade_report.html --self-contained-html
```

## Test Scenarios

### 1. Upgrade Scenarios

Each upgrade test follows this pattern:
1. **Install Old Version**: Install the specified old version
2. **Login**: Perform login with valid credentials
3. **Verify Login**: Confirm user is logged in and sees "My Devices"
4. **Upgrade**: Uninstall old version and install latest version
5. **Verify Upgrade**: Confirm user remains logged in after upgrade
6. **Error Check**: Verify no error dialogs appear

### 2. Clean Installation Scenarios

Tests upgrades without previous login:
1. **Install Old Version**: Install old version without logging in
2. **Upgrade**: Install latest version
3. **Verify Landing Screen**: Confirm app shows landing screen (not logged in)

### 3. Performance Tests

Measures timing for each step:
- Installation time
- Launch time
- Login time
- Upgrade time
- Verification time

### 4. Error Handling Tests

Tests error scenarios:
- Invalid APK paths
- Non-existent packages
- App launch failures

## Helper Functions

The `UpgradeHelpers` class provides utility functions:

```python
from helpers.upgrade_helpers import UpgradeHelpers

helper = UpgradeHelpers(driver)

# Install app version
helper.install_app_version(apk_path, package_name)

# Launch app
helper.launch_app(package_name)

# Verify user login
helper.verify_user_logged_in()

# Check for errors
error_messages = helper.check_for_error_dialogs()

# Take screenshot
helper.take_screenshot("debug.png")
```

## Test Results

### Success Criteria

✅ **Login Persistence**: User remains logged in after upgrade  
✅ **Device Access**: "My Devices" screen is visible  
✅ **No Errors**: No crash dialogs or error messages  
✅ **Performance**: Upgrade completes within reasonable time  

### Failure Indicators

❌ **Login Lost**: User is logged out after upgrade  
❌ **Screen Missing**: "My Devices" screen not visible  
❌ **Error Dialogs**: Crash dialogs or error messages appear  
❌ **Performance Issues**: Upgrade takes too long  

## Debugging

### Screenshots

Enable screenshot capture for debugging:

```bash
python -m pytest tests/test_upgrade_automation.py::TestUpgradeAutomation::test_upgrade_with_screenshot_capture -v
```

Screenshots are saved in `reports/screenshots/` directory.

### Logs

Check Appium logs in `appium.log` for detailed information.

### Version Status

Check available APK files:

```python
from config.app_versions import print_version_status
print_version_status()
```

## Integration with Existing Tests

The upgrade automation framework is designed to work alongside existing tests:

- **No Interference**: Uses separate test files and helpers
- **Shared Configuration**: Reuses existing capabilities and configuration
- **Common Helpers**: Extends existing helper functions
- **Isolated Execution**: Can be run independently or as part of test suite

## Continuous Integration

Add upgrade tests to CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Upgrade Tests
  run: |
    python -m pytest tests/test_upgrade_automation.py -v
    --html=reports/upgrade_report.html
    --self-contained-html
```

## Troubleshooting

### Common Issues

1. **APK Files Missing**
   - Ensure APK files are in `android/app/` directory
   - Check file names match configuration

2. **Appium Server Issues**
   - Restart Appium server
   - Check port 4725 is available

3. **Device Connection**
   - Ensure device/emulator is connected
   - Check ADB connection

4. **Login Failures**
   - Verify test credentials in configuration
   - Check network connectivity

### Performance Issues

- Increase timeouts in configuration
- Check device performance
- Monitor system resources

## Future Enhancements

- [ ] iOS upgrade testing support
- [ ] Network interruption simulation
- [ ] Multiple device testing
- [ ] Automated APK version detection
- [ ] Integration with CI/CD metrics
- [ ] Advanced error recovery scenarios

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review test logs and screenshots
3. Verify configuration and prerequisites
4. Check Appium and device connectivity
