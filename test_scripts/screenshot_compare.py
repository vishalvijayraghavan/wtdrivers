from WTDrivers import WTDrivers
from selenium import webdriver
import time

obj = WTDrivers()

src_image1 = "test_scripts/images/1504876269.0009959.png"
src_image2 = "test_scripts/images/1504876269.000995912.png"

if obj.screenshotCompare(src_image1, src_image2):
    print("images are same")
else:
    print("images not same")


