import os

#apk_path = os.getenv(
#    "APK_PATH",
#    os.path.abspath("/android/app/app-release.apk")
#)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apk_path = os.getenv(
    "APK_PATH",
    os.path.join(project_root, "android", "app", "app-release.apk")
)

android_caps = {
    "platformName": "Android",
    "deviceName": "emulator-5554",  # Or your actual emulator/device name
    "automationName": "UiAutomator2",
    "app": apk_path,

    # ✅ Launch behavior stabilizers
    "appWaitActivity": "*",
    "appWaitForLaunch": True,
    "autoLaunch": True,

    # ✅ State control
    "noReset": True,  # Use fullReset: True if you want a clean state each run
    # ✅ Permissions
    "autoGrantPermissions": True
}
