# Olarm Mobile Automation

A comprehensive mobile automation testing framework for the Olarm security system mobile application using Appium, Python, and pytest.

## 🚀 Features

- **Cross-Platform Testing**: Android mobile app automation
- **Page Object Model**: Organized, maintainable test structure
- **Comprehensive Test Coverage**: Login, device setup, zones, areas, notifications, and more
- **Advanced Navigation**: Smart modal dismissal and back navigation handling
- **Upgrade Testing**: Automated app upgrade verification across multiple versions
- **Allure Reporting**: Detailed test reports with screenshots
- **Session Management**: Efficient test execution with shared sessions

## 📋 Prerequisites

- **Python 3.9+**
- **Node.js** (for Appium)
- **Android SDK**
- **Appium Server**
- **Android Device/Emulator**

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/OlarmTech/olarm-mobile-automation.git
cd olarm-mobile-automation
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Appium
```bash
npm install -g appium
appium driver install uiautomator2
```

### 5. Setup Configuration
```bash
python setup_email_config.py  # For email reporting (optional)
```

## 🔧 Configuration

### Device Configuration
Update `config/capabilities.py` with your device details:
```python
CAPABILITIES = {
    'platformName': 'Android',
    'deviceName': 'YOUR_DEVICE_NAME',
    'app': '/path/to/app-release.apk',
    # ... other capabilities
}
```

### Test Data
Configure test credentials in `testdata/login_data.json`:
```json
{
    "valid_user": {
        "email": "your-test-email@example.com",
        "password": "your-test-password"
    }
}
```

## 🏃‍♂️ Running Tests

### Start Appium Server
```bash
appium
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Suites
```bash
# Zone functionality tests
pytest tests/MGSP/SP6000+/SP6000+_zones_tests.py -v

# Arm/Disarm tests  
pytest tests/MGSP/SP6000+/SP6000+_Arm_tests.py -v

# Burger menu tests
pytest tests/Burger_menu_items/ -v

# Search zones test
pytest tests/MGSP/SP6000+/SP6000+_zones_tests.py::test_search_zones -v
```

### Run with Allure Reporting
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Run Upgrade Tests
```bash
python run_upgrade_tests.py
python run_upgrade_tests_with_email.py  # With email reporting
```

## 📁 Project Structure

```
olarm-mobile-automation/
├── android/app/                    # APK files for different versions
├── config/                         # Configuration files
│   ├── capabilities.py            # Device capabilities
│   ├── environment.py             # Environment settings
│   └── app_versions.py            # App version mappings
├── drivers/                        # WebDriver factory
├── helpers/                        # Common test utilities
│   ├── common_tests.py            # Shared test functions
│   └── upgrade_helpers.py         # Upgrade test utilities
├── pages/                          # Page Object Model
│   ├── base_page.py               # Base page class
│   ├── login_page.py              # Login functionality
│   ├── zones_page.py              # Zones management
│   ├── areas_page.py              # Areas/arming functionality
│   ├── burger_menu_page.py        # Navigation menu
│   └── device_setup_page.py       # Device setup flows
├── tests/                          # Test suites
│   ├── MGSP/SP6000+/              # SP6000+ panel tests
│   ├── Burger_menu_items/         # Navigation menu tests
│   └── debug_test_files/          # Debug utilities
├── testdata/                       # Test data files
├── utils/                          # Utility functions
├── reports/                        # Test reports and screenshots
└── requirements.txt               # Python dependencies
```

## 🧪 Key Test Features

### Zone Search Functionality
```python
# Search for specific zones
page = ZonesPage(driver)
page.search_zones("Zone 06")
```

### Smart Modal Dismissal
```python
# Automatically handles various modal dismissal methods
page = BurgerMenuPage(driver)
page.dismiss_device_notifications_modal()
```

### Navigation Management  
```python
# Navigate back from webviews and modals
page.navigate_back_from_terms_of_service()
```

### Upgrade Testing
```python
# Test app upgrades across versions
python run_upgrade_tests.py
```

## 🔍 Recent Improvements

- ✅ **Fixed Zone Search**: Corrected `search_zones()` method to use proper text input
- ✅ **Enhanced Navigation**: Added robust back navigation for Terms of Service webviews
- ✅ **Modal Management**: Implemented smart modal dismissal with multiple fallback strategies
- ✅ **Test Stability**: Fixed driver reference issues and improved test reliability
- ✅ **Expanded Coverage**: Added support for additional zones (07, 08, 09)

## 📊 Test Reporting

### Allure Reports
Generate beautiful test reports with:
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Email Reports
Configure and send automated email reports:
```bash
python run_upgrade_tests_with_email.py
```

### Screenshots
Automatic screenshot capture on failures stored in:
- `reports/screenshots/`
- `upgrade_screenshots/`

## 🛠️ Debugging

### Debug Tests
```bash
# Debug current screen elements
pytest tests/debug_test_files/debug_current_screen.py -v -s

# Debug zones functionality  
pytest tests/debug_test_files/debug_zones_tabs.py -v -s
```

### Common Issues

1. **App Not Found**: Ensure APK path in capabilities is correct
2. **Element Not Found**: Check if app UI has changed, update locators
3. **Session Issues**: Restart Appium server and clear app data
4. **Permission Dialogs**: Tests handle Android permission dialogs automatically

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

### Code Standards
- Follow PEP 8 style guidelines
- Use Page Object Model pattern
- Include docstrings for methods
- Add appropriate wait times for UI operations
- Handle exceptions gracefully

## 📄 License

This project is proprietary to OlarmTech.

## 📞 Support

For issues and support:
- Create GitHub issues for bugs
- Contact the QA team for test-related questions
- Review existing test documentation in `UPGRADE_AUTOMATION_README.md`

---

**Built with ❤️ by the Olarm QA Team**
