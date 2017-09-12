from WTDrivers import WTDrivers
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.youtube.com/')


obj = WTDrivers(driver,filetype=".png",filepath="./tmp/images/")  #filepath:where all the images will be stored


sub_image = "test_scripts/images/icon.png"

xy_list = obj.findSubImageCordinates(sub_image) #this function will internally call fullscreenshot() and locate the subimage on fullscreenshot image and return its co-ordinates

obj.clickCoordinates(xy_list[0])    #click the given co-ordinate

driver.close()



