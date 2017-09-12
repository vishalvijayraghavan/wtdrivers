from WTDrivers import WTDrivers
from selenium import webdriver
import time

#selenium create driver object
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://www.youtube.com/')

obj = WTDrivers(driver,filetype=".png",filepath="./tmp/images/")  #filepath:where all the images will be stored

list_obj = obj.fullAutomationMode(dimensions=[53,236,197,597],resize_size=5,enhance_by=30.0,flag='xy')  #will return dict of (x,y) co-ordinates for elements in navbar

#list_obj = obj.fullAutomationMode(dimensions=[53,236,197,597],resize_size=5,enhance_by=30.0,flag='xy') #will return xpath selenium objects for elements in navbar

for i in list_obj:
    obj.clickCoordinates(list_obj[i])  # will click all the x,y given
    #list_obj[i].click()  #if xpath objects are used
    time.sleep(10)

driver.close()