import time

from helpers.common_tests import select_device, first_login_btn, do_login, do_disarm
from pages.areas_page import AreasPage


def test_stay_arm(driver):
    first_login_btn(driver)
    do_login(driver)
    select_device(driver)
    page = AreasPage(driver)
    page.stay_arm()
    info = page.get_area_info_by_label("Front Door")
    assert info["status"] == "Stay Armed"
    assert "Now" in info["time"]
    time.sleep(3)

def test_sleep_arm(driver):
   # first_login_btn(driver)
    #do_login(driver)
    #select_device(driver)
    page = AreasPage(driver)
    page.sleep_arm()
    info = page.get_area_info_by_label("Front Door")
    assert info["status"] == "Sleep Armed"
    assert "Now" in info["time"]

def test_disarm(driver):
    do_disarm(driver)
    page = AreasPage(driver)
    info = page.get_area_info_by_label("Front Door")
    assert info["status"] == "Disarmed"
    assert "Now" in info["time"]
    time.sleep(30)

def test_reset_app(driver_with_uninstall):
    # This test will uninstall the app after it runs
    ...