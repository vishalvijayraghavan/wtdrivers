from WTDrivers import WTDrivers
from selenium import webdriver
import time

obj = WTDrivers()

src_image = "test_scripts/images/dashboard.png"

text_list = obj.extractTextFromImage(src_image) #this function extract all the text from given image and return the list of all

print(text_list)


