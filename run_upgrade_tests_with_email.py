#!/usr/bin/env python3
"""
Test runner script for Olarm mobile app upgrade tests with email reporting
"""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.email_sender import EmailSender
from config.email_config import get_email_config, validate_email_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('upgrade_tests.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class UpgradeTestRunner:
    """Test runner for upgrade tests with email reporting"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'total': 0
        }
        self.email_sender = None
        self.setup_email()
    
    def setup_email(self):
        """Setup email sender with configuration"""
        try:
            config = get_email_config()
            is_valid, error_msg = validate_email_config(config)
            
            if not is_valid:
                logger.warning(f"Email configuration invalid: {error_msg}")
                logger.info("Email reporting will be disabled. Update config/email_config.py with your email settings.")
                return
            
            self.email_sender = EmailSender(config)
            
            # Test email connection
            if self.email_sender.test_connection():
                logger.info("✅ Email configuration is valid and connection test successful")
            else:
                logger.warning("⚠️ Email connection test failed. Email reporting will be disabled.")
                self.email_sender = None
                
        except Exception as e:
            logger.error(f"Failed to setup email: {e}")
            self.email_sender = None
    
    def run_tests(self):
        """Run all upgrade tests"""
        logger.info("🚀 Starting Olarm Mobile App Upgrade Tests")
        self.start_time = time.time()
        
        # Clean previous results
        self.clean_previous_results()
        
        # Run in-place upgrade tests
        logger.info("📋 Running in-place upgrade tests...")
        inplace_results = self.run_test_suite("tests/test_upgrade_automation.py")
        
        # Run clean installation tests
        logger.info("📋 Running clean installation tests...")
        clean_results = self.run_test_suite("tests/test_app_upgrade.py::TestAppUpgrade::test_upgrade_clean_installation")
        
        # Combine results
        self.test_results = self.combine_results(inplace_results, clean_results)
        
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        logger.info(f"✅ All tests completed in {duration:.2f} seconds")
        logger.info(f"📊 Results: {self.test_results['passed']} passed, {self.test_results['failed']} failed, {self.test_results['skipped']} skipped")
        
        # Generate Allure report
        self.generate_allure_report()
        
        # Send email report
        self.send_email_report(duration)
        
        return self.test_results
    
    def clean_previous_results(self):
        """Clean previous test results"""
        allure_results_dir = "reports/allure-results"
        if os.path.exists(allure_results_dir):
            import shutil
            shutil.rmtree(allure_results_dir)
            logger.info("🧹 Cleaned previous allure-results")
        
        os.makedirs(allure_results_dir, exist_ok=True)
    
    def run_test_suite(self, test_path):
        """Run a specific test suite"""
        cmd = [
            sys.executable, "-m", "pytest",
            test_path,
            "-v",
            "--alluredir=./reports/allure-results",
            "--tb=short"
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=project_root
            )
            
            # Parse results from output
            results = self.parse_pytest_output(result.stdout)
            
            if result.returncode == 0:
                logger.info(f"✅ {test_path} completed successfully")
            else:
                logger.warning(f"⚠️ {test_path} had some failures")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to run {test_path}: {e}")
            return {'passed': 0, 'failed': 1, 'skipped': 0, 'total': 1}
    
    def parse_pytest_output(self, output):
        """Parse pytest output to extract test results"""
        results = {'passed': 0, 'failed': 0, 'skipped': 0, 'total': 0}
        
        # Look for summary line like: "6 passed, 2 skipped, 1 warning in 269.05s"
        import re
        summary_pattern = r'(\d+) passed.*?(\d+) failed.*?(\d+) skipped'
        match = re.search(summary_pattern, output)
        
        if match:
            results['passed'] = int(match.group(1))
            results['failed'] = int(match.group(2)) if match.group(2) else 0
            results['skipped'] = int(match.group(3)) if match.group(3) else 0
            results['total'] = results['passed'] + results['failed'] + results['skipped']
        
        return results
    
    def combine_results(self, results1, results2):
        """Combine results from multiple test suites"""
        combined = {
            'passed': results1.get('passed', 0) + results2.get('passed', 0),
            'failed': results1.get('failed', 0) + results2.get('failed', 0),
            'skipped': results1.get('skipped', 0) + results2.get('skipped', 0),
            'total': 0
        }
        combined['total'] = combined['passed'] + combined['failed'] + combined['skipped']
        return combined
    
    def generate_allure_report(self):
        """Generate Allure report"""
        logger.info("📊 Generating Allure report...")
        
        cmd = [
            "allure", "generate",
            "./reports/allure-results",
            "--clean",
            "-o", "./reports/allure-report"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
            
            if result.returncode == 0:
                logger.info("✅ Allure report generated successfully")
            else:
                logger.error(f"Failed to generate Allure report: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Failed to generate Allure report: {e}")
    
    def send_email_report(self, duration):
        """Send email report"""
        if not self.email_sender:
            logger.info("📧 Email reporting is disabled (no valid email configuration)")
            return
        
        logger.info("📧 Sending email report...")
        
        test_summary = {
            'passed': self.test_results['passed'],
            'failed': self.test_results['failed'],
            'skipped': self.test_results['skipped'],
            'total': self.test_results['total'],
            'duration': f"{duration:.2f} seconds"
        }
        
        allure_results_dir = "reports/allure-results"
        allure_report_dir = "reports/allure-report"
        
        if os.path.exists(allure_report_dir):
            success = self.email_sender.send_allure_report(
                allure_results_dir,
                allure_report_dir,
                test_summary
            )
            
            if success:
                logger.info("✅ Email report sent successfully")
            else:
                logger.error("❌ Failed to send email report")
        else:
            logger.error("❌ Allure report directory not found")
    
    def open_report(self):
        """Open Allure report in browser"""
        report_dir = "reports/allure-report"
        
        if os.path.exists(report_dir):
            logger.info("🌐 Opening Allure report in browser...")
            
            try:
                subprocess.run(["allure", "open", report_dir], cwd=project_root)
            except Exception as e:
                logger.error(f"Failed to open report: {e}")
        else:
            logger.error("❌ Allure report not found")

def main():
    """Main function"""
    print("=" * 60)
    print("🚀 Olarm Mobile App Upgrade Test Runner")
    print("=" * 60)
    
    runner = UpgradeTestRunner()
    
    try:
        # Run tests
        results = runner.run_tests()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST EXECUTION SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⏭️ Skipped: {results['skipped']}")
        print(f"📈 Total: {results['total']}")
        
        if results['failed'] == 0:
            print("\n🎉 All tests passed successfully!")
        else:
            print(f"\n⚠️ {results['failed']} tests failed")
        
        # Ask if user wants to open report
        response = input("\n🌐 Open Allure report in browser? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            runner.open_report()
        
    except KeyboardInterrupt:
        logger.info("Test execution interrupted by user")
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


