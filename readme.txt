#WTDrivers

#Dependencies Installation:

- Following script will install all system and python dependencies required by script
    > sudo python3 setup/setup.py

- used chrome plugin coordinates to get the co-ordinates
    - https://chrome.google.com/webstore/detail/coordinates/bpflbjmbfccblbhlcmlgkajdpoiepmkd

#Usecase:

    - If we have a dashboard with navigation bar and want to itterate through all the option on it so what is the possible way to acheive it ?
    Ans : we will have xpath of all the elements on navigation menu and then using webdriver itterate through it.
        But what if
        i. id/class/any attribute changes
        ii. if the UI changes
        iii. if new element is added or removed from UI , then entire automation script might wont work as aspected.

    - In regration testing insted of testing whole website again and again we can use spanshot testing ( screenshotCompare() )
    where in we can compare the screenshot of current release and stable release and check if ui changed or not
    - click on x,y coordinates not possible in native selenium but with this framework it is possible
    - OCR for webpage screenshot
    - automate UI just by giving the any element image on screen


#Functions:

    -fullAutomationMode():This is full automated function which will locate object in the given dimensions and return their co-ordinate or xpath objects
        :param dimensions: dimensions to be worked on (top left x co-ordinate,top left y co-ordinate,buttom right x co-ordinate,buttom right y co-ordinate)
        :param resize_size: resize image by n times
        :param enhance_by: enhance image by n time
        :param flag : what you want to return dictionary of xpath objects or x,y coordinates ('xy':for cordinates , 'objects':for xpath objects)
        :return: return a dictionary {"element_name":<xpath object>}  / {"element_name":(x,y)}

    -screenshotCompare():This function will compare two images pixel by pixel and return true or false
        :param src_image1:
        :param src_image2:
        :return: true/false

    -findSubImageCordinates():This function is used to find if an image consist of subimage if yes return the co-ordinates
        :param subimage: sub-image which you want to find inside the fullpage image
        :return: list of co-ordinates(tuples with x,y co-ord) found

    -clickCoordinates():This function will click on the cordinates given
        :param coordinates: {'x':1,'y':2} or (1,2) or [1,2] or [(0,1)]  co-ordinates
        :return: false if not valid input else true
