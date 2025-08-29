#!/usr/bin/env python3
"""
Simple Upgrade Test Runner
"""

import os
import sys
import subprocess
from config.app_versions import print_version_status, get_available_versions


def main():
    """Main function to run upgrade tests"""
    print("🚀 Upgrade Automation Test Runner")
    print("=" * 50)
    
    # Print version status
    print_version_status()
    
    # Check available versions
    available_versions = get_available_versions()
    if not available_versions:
        print("❌ No APK files found. Please ensure APK files are in android/app/ directory")
        sys.exit(1)
    
    # Build pytest command
    cmd = [
        "python", "-m", "pytest",
        "tests/test_upgrade_automation.py",
        "-v",
        "--html=reports/upgrade_report.html",
        "--self-contained-html"
    ]
    
    print(f"\n🚀 Running tests with command: {' '.join(cmd)}")
    print("=" * 80)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Tests completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
