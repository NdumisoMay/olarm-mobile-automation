from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.capabilities import android_caps
#
def init_driver():
     options = UiAutomator2Options()
     for k, v in android_caps.items():
         options.set_capability(k, v)

     # ✅ Connect to default path — NOT /wd/hub
     return webdriver.Remote("http://localhost:4723", options=options)

