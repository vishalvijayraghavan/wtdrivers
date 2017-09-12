import pytesseract
import time, os, json, logging, sys
import numpy as np
from PIL import Image, ImageEnhance, ImageChops
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WTDrivers:

    def __init__(self, driver, filetype=".png", filepath="./tmp/"):
        '''
        This is webdriver object for selenium
        :param driver:
        '''

        self.driver = driver
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        self.filetype = filetype
        self.filepath = filepath
        logging.basicConfig(filename='./SnapshotModule.log', filemode='w', level=logging.INFO)
        logging.info("Logging for " + time.ctime())


    def fullpageSnapshot(self, filename=time.time()):
        '''
        This function will take entire screenshot.
        :param filename: file to save screenshot image (optional)
        :return: fullpage screenshot image object and image name
        '''

        try:

            logging.info("full screenshot method initializing")
            FQ_filename = self.filepath + str(filename) + self.filetype
            self.driver.get_screenshot_as_file(FQ_filename)
            image = Image.open(FQ_filename)  # open that image
            logging.info("full screenshot completed")

            return {"image_object": image, "image_name": FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)


    def imageCleaner(self, src_image, resize_size=3, enhance_by=30.0, filename=time.time()):
        '''
        This function will clean the image
        i.e - it will resize the image by 3 times
            - sharpen the image
            - invert the image(black and white image)
        :param src_image_object: source image object
        :param resize_size: zoomout image by (default 3) (optional)
        :param enhance_by: enhance rate (default 30.0) (optional)
        :param filename: cleaned image save to this filename (optional)
        :return: dictionary with image_object & image_path
        '''


        if not isinstance(enhance_by, float):
            logging.error("invalid enhance_by given to imageCleaner()")
            #sys.exit()
            return False

        if not isinstance(resize_size, int):
            logging.error("invalid enhance_by given to imageCleaner()")
            #sys.exit()
            return False

        if src_image == "":
            logging.error("src image required to imageCleaner()")
            #sys.exit()
            return False

        self.src_image_object = self.checkImageOrObject(src_image)

        try:

            logging.info("ImageCleaner method initializing")
            src_image = self.src_image_object.resize((self.src_image_object.width * resize_size, self.src_image_object.height * resize_size), Image.ANTIALIAS)
            enhancer = ImageEnhance.Sharpness(src_image)
            src_image = enhancer.enhance(enhance_by)
            logging.info("Image enhance completed")
            src_image = src_image.convert('L')

            src_image = src_image.point(lambda x: 0 if x < 175 else 255, '1')
            # src_image   = src_image.point(range(256, 0, -1) * 3)

            FQ_filename = self.filepath + str(filename) + self.filetype
            src_image.save(FQ_filename)
            logging.info("Image Cleaning completed")

            return {'image_object': src_image, 'image_path': FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)


    def extractTextFromImage(self, src_image):
        """
        This function using tesseract engine pytesseract(python wrapper) will extract the text from image
         and return the list of text extracted
        :param src_image:
        :return:extracted text list
        """

        if src_image == "":
            logging.error("src image required to extractTextFromImage()")
            sys.exit()
            #return False

        self.src_image_object = self.checkImageOrObject(src_image)


        try:

            logging.info("ExtractTextFromImage method initializing")

            text_str = pytesseract.image_to_string(self.src_image_object)
            str_list = text_str.split("\n")
            str_list = list(filter(None, str_list))  # remove empty string
            logging.info("ExtractTextFromImage completed : " + str(str_list))
            return str_list
        except Exception as e:
            logging.info(e)
            print(e)


    def cropImage(self, src_image, dimensions, filename=time.time()):
        '''
        This function will crop the image as per image and dimentions provided
        :param src_image_object:
        :param dimensions:
        :param filename: (optional)
        :return: dict{image_object,image_name}
        '''


        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to cropImage()")
                sys.exit()
                #return False
        else:
            logging.error("invalid dimensions given to cropImage() ")
            sys.exit()
            #return False

        if src_image == "":
            logging.error("src image required to cropImage()")
            sys.exit()
            #return False

        self.src_image_object = self.checkImageOrObject(src_image)


        try:
            logging.info("CropImage method initializing")

            FQ_filename = self.filepath + str(filename) + self.filetype
            cropped_img = self.src_image_object.crop(dimensions)  # crop the required section from image
            cropped_img.save(FQ_filename)
            logging.info("CropImage Completed")

            return {"image_object": cropped_img, "image_name": FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)


    def getTextXpathObject(self, text, dimensions, flag=1):
        '''
        This function will get the location of text as per the dimentions provided on page and return the object of that text
        :param text:
        :param dimensions:
        :param flag : if flag = 1 return xpath object or (x,y) co-ordinates
        :return: return the object of that text if in dimension else return false
        '''

        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to getTextXpathObject()")
                sys.exit()
                #return False
        else:
            logging.error("invalid dimensions given to getTextXpathObject() ")
            sys.exit()
            #return False

        if not isinstance(text, str):
            logging.error("text aspected as an input to getTextXpathObject()")
            sys.exit()
            #return False

        try:

            logging.info("getTextLocationObject method initializing")
            text_list = self.driver.find_elements_by_xpath("//*[contains(text(), '" + text + "')]")
            logging.info(text + " found @ " + str(len(text_list)) + " locations")
            for txt in text_list:
                txt_location = txt.location
                print(text + 'found @' + str(txt_location))
                if (txt_location['x'] >= dimensions[0] and txt_location['y'] >= dimensions[1] and txt_location['x'] <=
                    dimensions[2] and txt_location['y'] <= dimensions[3]):
                    # print("our text @ "+str(txt_location))
                    logging.info(text + " found @ " + str(txt_location))

                    if flag == 1:
                        return txt
                    else:
                        return txt_location

            logging.info(text + " not found in given dimention")
            return False

        except Exception as e:
            logging.info(e)
            print(e)


    def getTextXpathObjects(self, text_list, dimensions, flag=1):
        '''
        This function will get the location of text as per the dimension provided on page and return the object of that text
        :param text_list:
        :return: return the object of that text if in dimension else return false
        '''

        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to getTextXpathObjects()")
                sys.exit()
                #return False
        else:
            logging.error("invalid dimensions given to getTextXpathObjects() ")
            sys.exit()
            #return False

        if not isinstance(text_list, list):
            logging.error("invalid input given list expected to getTextXpathObjects()")
            sys.exit()
            #return False

        try:
            final_obj_dict = {}

            logging.info("getTextLocationObject method initializing")
            for text in text_list:  # each text iterate
                text_obj = self.getTextXpathObject(text, dimensions, flag)
                if (text_obj):
                    final_obj_dict[text] = text_obj
                    # logging.info(text+" not found in given dimention")

            return final_obj_dict

        except Exception as e:
            logging.info(e)
            print(e)


    def getTextCordinate(self, text, dimensions):
        '''
        This function will return the x & y co-ordinates for element provided
        :param text:
        :param dimensions:
        :return: {'label': {'y': 370, 'x': 72}}
        '''

        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to getTextCordinate()")
                sys.exit()
                #return False
        else:
            logging.error("invalid dimensions given to getTextCordinate() ")
            sys.exit()
            #return False

        if not isinstance(text, str):
            logging.error("text aspected as an input to getTextCordinate()")
            sys.exit()
            #return False

        return self.getTextXpathObject(text, dimensions, 0)


    def getTextCordinates(self, text_list, dimensions):
        '''
        This function will return x & y coordinates for list of elements provided
        :param text_list:
        :param dimensions:
        :return: {'label': {'y': 370, 'x': 72}}
        '''

        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to getTextCordinates()")
                sys.exit()
                #return False
        else:
            logging.error("invalid dimensions given to getTextCordinates() ")
            sys.exit()
            #return False

        if not isinstance(text_list, list):
            logging.error("invalid input given list expected to getTextCordinates()")
            sys.exit()
            #return False

        return self.getTextXpathObjects(text_list, dimensions, 0)


    def fullAutomationMode(self, dimensions=[0, 0, 0, 0], resize_size=5, enhance_by=30.0, flag='objects'):

        '''
        This is full automated function in which all the config is taken from config file and object is located
        :param dimensions: dimensions to be worked on (top left x co-ordinate,top left y co-ordinate,buttom right x co-ordinate,buttom right y co-ordinate)
        :param resize_size: resize image by n times
        :param enhance_by: enhance image by n time
        :param flag : what you want to return dictionary of xpath objects or x,y coordinates
        :return: return a dictionary {"element_name":<xpath object>}
        '''

        if isinstance(dimensions, list) or isinstance(dimensions, tuple):
            if not len(dimensions) == 4:
                logging.error("invalid dimensions given to fullAutomaitonMode()")
                return False
        else:
            logging.error("invalid dimensions given to fullAutomaitonMode() ")
            return False

        if not isinstance(enhance_by,float):
            logging.error("invalid enhance_by given to fullAutomaitonMode()")
            return False
        if not isinstance(resize_size, int):
            logging.error("invalid enhance_by given to fullAutomaitonMode()")
            return False

        if isinstance(flag, str):
            if flag == 'objects' or flag == 'xy':
                pass
            else:
                logging.error("flag value can be either 'objects' or 'xy' ")
                return False

        try:
            logging.info("initializing all global varibles")
            self.resize_size = resize_size
            self.enhance_by = enhance_by
            self.dimensions = dimensions

            fullpage = self.fullpageSnapshot()
            cropped = self.cropImage(fullpage['image_object'], self.dimensions)
            enhance = self.imageCleaner(cropped['image_object'], self.resize_size, self.enhance_by)
            text_list = self.extractTextFromImage(enhance['image_object'])
            if flag == 'xy':
                return self.getTextCordinates(text_list, self.dimensions)
            else:
                return self.getTextLocationObjects(text_list, self.dimensions)

        except Exception as e:
            logging.info(e)
            print(e)


    def checkImageOrObject(self,src_image):
        '''
        This function will check if the src_image passed to this function is filepath or image file object.
        if image file path found it will open file and return file object else return image file object
        :param src_image:
        :return: return image file object
        '''

        try:

            if type(src_image) == str:
                if not os.path.exists(src_image):
                    logging.error("invalid image path given ")
                    print("invalid image path given")
                    sys.exit()
                    # return False
                else:
                    return Image.open(src_image)
            else:
                return src_image

        except Exception as e:
            print(e)
            logging.error(e)


    def screenshotCompare(self, src_image1, src_image2):
        '''
        This function will compare two images pixel by pixel and return true or false
        :param src_image1:
        :param src_image2:
        :return: true/false
        '''

        if (not os.path.exists(src_image1)) or (not os.path.exists(src_image2)):
            logging.error("invalid image path given to screenshotCompare()")
            print("invalid image path given to screenshotCompare()")
            # self.driver.execute_script("alert('Error occured plz verify and rerun script !!!');")
            return False


        try:

            img1 = self.checkImageOrObject(src_image1)
            img2 = self.checkImageOrObject(src_image2)

            diff = ImageChops.subtract(img1, img2)

            if not diff.getbbox():
                print("same")
                return True
            else:
                print("not same")
                return False

        except Exception as e:
            logging.info(e)
            print(e)


    def findSubImageCordinates(self, subimage):

        '''
        This function is used to find if an image consist of subimage if yes return the co-ordinates
        :param subimage: sub-image which you want to find inside the fullpage image
        :return: list of co-ordinates(tuples with x,y co-ord) found
        '''

        if not os.path.exists(subimage):
            logging.error("invalid subimage path given to findSubImageCordinates()")
            print("invalid subimage path given to findSubImageCordinates()")
            # self.driver.execute_script("alert('Error occured plz verify and rerun script !!!');")
            return False

        # get screenshot and get its open image object
        fullpage = self.fullpageSnapshot()
        fullscreenshot_image_object = fullpage['image_object']

        subimage_object = self.checkImageOrObject(subimage)

        # create image array for manipulation
        arr_f = np.asarray(fullscreenshot_image_object)
        arr_s = np.asarray(subimage_object)

        # Get the dimensions of the numpy image array
        y_f, x_f = arr_f.shape[:2]
        y_s, x_s = arr_s.shape[:2]

        xstop = x_f - x_s + 1
        ystop = y_f - y_s + 1

        matches = []

        for xmin in range(0, xstop):
            for ymin in range(0, ystop):
                xmax = xmin + x_s
                ymax = ymin + y_s

                arr_sub = arr_f[ymin:ymax, xmin:xmax]  # extract subimage
                arr_t = (arr_sub == arr_s)  # create test matrix
                if arr_t.all():  # test whether all array elements along a given axis evaluate to True and only consider exact matches
                    matches.append((xmin, ymin))

        return matches


    def clickCoordinates(self, coordinates):

        '''
        This function will click on the cordinates given
        :param coordinates: {'x':1,'y':2} or (1,2) or [1,2] or [(0,1)]  co-ordinates
        :return: false if not valid input else true
        '''

        # selenium does not have pure co-ordinate based click event so using javascript to achive this
        if isinstance(coordinates, dict):  # {'x':1,'y':2}

            self.driver.execute_script(
                'document.elementFromPoint(' + str(coordinates["x"]) + ',' + str(coordinates["y"]) + ').click();')

        elif isinstance(coordinates, tuple):  # (1,2)
            self.driver.execute_script(
                'document.elementFromPoint(' + str(coordinates[0]) + ',' + str(coordinates[1]) + ').click();')

        elif isinstance(coordinates, list):  # []

            if isinstance(coordinates[0], int):  # [1,2]
                self.driver.execute_script(
                    'document.elementFromPoint(' + str(coordinates[0]) + ',' + str(coordinates[1]) + ').click();')
            elif isinstance(coordinates[0], tuple):  # [(0,1)]
                self.driver.execute_script(
                    'document.elementFromPoint(' + str(coordinates[0][0]) + ',' + str(coordinates[0][1]) + ').click();')
            else:
                print('Invalid input co-ordinates')
                logging.info('Invalid input co-ordinates')
                return False
        else:
            print('Invalid input co-ordinates')
            logging.info('Invalid input co-ordinates')
            return False

        time.sleep(2)

        return True

