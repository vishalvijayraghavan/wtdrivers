import pytesseract
import time,os,json,logging
import numpy as np
from PIL import Image,ImageEnhance,ImageChops

class SnapshotModulev1:

    def __init__(self,driver):
        '''
        This is webdriver object for selenium
        :param driver:
        '''

        self.driver = driver

        logging.basicConfig(filename='./SnapshotModule.log', filemode='w', level=logging.INFO)
        logging.info("Logging for "+time.ctime())

        self.filetype = '.png'
        self.filepath = './testing/'



    def fullpageSnapshot(self,filename=time.time()):
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

            return {"image_object":image,"image_name":FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)


    def imageCleaner(self,src_image_object,resize_size=3,enhance_by=30.0,filename=time.time()):
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

        try:

            logging.info("ImageCleaner method initializing")
            src_image   = src_image_object.resize((src_image_object.width * resize_size, src_image_object.height * resize_size), Image.ANTIALIAS)
            enhancer    = ImageEnhance.Sharpness(src_image)
            src_image   = enhancer.enhance(enhance_by)
            logging.info("Image enhance completed")
            src_image   = src_image.convert('L')

            src_image   = src_image.point(lambda x: 0 if x < 175 else 255, '1')
            #src_image   = src_image.point(range(256, 0, -1) * 3)

            FQ_filename = self.filepath+str(filename)+self.filetype
            src_image.save(FQ_filename)
            logging.info("Image Cleaning completed")

            return {'image_object':src_image,'image_path':FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)

    def extractTextFromImage(self,src_image_object):
        """
        This function using tesseract engine pytesseract(python wrapper) will extract the text from image
         and return the list of text extracted
        :param src_image_object:
        :return:extracted text list
        """
        try:

            logging.info("ExtractTextFromImage method initializing")

            text_str = pytesseract.image_to_string(src_image_object)
            str_list = text_str.split("\n")
            str_list = list(filter(None, str_list)) #remove empty string
            logging.info("ExtractTextFromImage completed : " + str(str_list))
            return str_list
        except Exception as e:
            logging.info(e)
            print(e)

    def cropImage(self,src_image_object,dimensions,filename=time.time()):
        '''
        This function will crop the image as per image and dimentions provided
        :param src_image_object:
        :param dimensions:
        :param filename: (optional)
        :return: dict{image_object,image_name}
        '''

        try:
            logging.info("CropImage method initializing")

            FQ_filename = self.filepath + str(filename) + self.filetype
            cropped_img = src_image_object.crop(dimensions)  # crop the required section from image
            cropped_img.save(FQ_filename)
            logging.info("CropImage Completed")

            return {"image_object":cropped_img,"image_name":FQ_filename}

        except Exception as e:
            logging.info(e)
            print(e)


    def getTextLocationObject(self,text,dimensions):
        '''
        This function will get the location of text as per the dimentions provided on page and return the object of that text
        :param text:
        :param dimensions:
        :return: return the object of that text if in dimension else return false
        '''

        try:

            logging.info("getTextLocationObject method initializing")
            text_list = self.driver.find_elements_by_xpath("//*[contains(text(), '"+text+"')]")
            logging.info(text+" found @ "+str(len(text_list))+" locations")
            for txt in text_list:
                txt_location = txt.location
                print(text+'found @'+str(txt_location))
                if(txt_location['x'] >= dimensions[0] and txt_location['y'] >= dimensions[1] and txt_location['x'] <= dimensions[2] and txt_location['y'] <= dimensions[3]):
                    #print("our text @ "+str(txt_location))
                    logging.info(text + " found @ " + str(txt_location))
                    return txt
            logging.info(text+" not found in given dimention")
            return False

        except Exception as e:
            logging.info(e)
            print(e)


    def getTextLocationObjects(self,text_list,dimensions):
        '''
        This function will get the location of text as per the dimension provided on page and return the object of that text
        :param text_list:
        :return: return the object of that text if in dimension else return false
        '''

        try:
            final_obj_dict = {}

            logging.info("getTextLocationObject method initializing")
            for text in text_list:    #each text iterate
                # individual_text_list = self.driver.find_elements_by_xpath("//*[contains(text(), '"+text+"')]")
                # logging.info(text+" found @ "+str(len(text_list))+" locations")
                # for txt in individual_text_list:    #iterate through the occurances
                #     txt_location = txt.location     #get x,y co-ordinate of that text
                #     print(text+'found @'+str(txt_location))
                #     if(txt_location['x'] >= dimensions[0] and txt_location['y'] >= dimensions[1] and txt_location['x'] <= dimensions[2] and txt_location['y'] <= dimensions[3]):
                #         #print("our text @ "+str(txt_location))
                #         logging.info("exact "+text + " found @ " + str(txt_location))
                #         final_obj_dict[text] = txt

                text_obj = self.getTextLocationObject(text,dimensions)
                if(text_obj):
                    final_obj_dict[text] = text_obj
                #logging.info(text+" not found in given dimention")

            return final_obj_dict

        except Exception as e:
            logging.info(e)
            print(e)

    def fullAutomationMode(self):
        '''
        This is full automated function in which all the config is taken from config file and object is located
        :return: return a dictionary {"element_name":<xpath object>}
        '''

        try:
            logging.info("initializing all global varibles")

            if os.path.isfile('./SnapshotModuleConfig.json'):
                logging.info("config file exist")
                with open('./SnapshotModuleConfig.json') as data_file:
                    config = json.load(data_file)
            else:
                logging.info("creating config file @ "+os.getcwd())
                config = {"filetype":".png","filepath":"/tmp/","resize_size":3,"enhance_by":30.0,"dimensions":[0,0,0,0]}
                with open('./SnapshotModuleConfig.json', 'w') as outfile:
                    json.dump(config, outfile)


            # self.filetype       = config['filetype']
            # self.filepath       = config['filepath']+"/"
            # self.resize_size    = config['resize_size']
            # self.enhance_by     = config['enhance_by']
            # self.dimensions     = config['dimensions']
            self.config = config
            if os.path.isdir(self.config['filepath']):
                pass
            else:
                os.makedirs(self.config['filepath'])

        except Exception as e:
            logging.info(e)
            print(e)

        fullpage    = self.fullpageSnapshot()
        cropped     = self.cropImage(fullpage['image_object'],config['dimensions'])
        enhance     = self.imageCleaner(cropped['image_object'],self.config['resize_size'],self.config['enhance_by'])
        text_list   = self.extractTextFromImage(enhance['image_object'])

        return self.getTextLocationObjects(text_list,config['dimensions'])

    def screenshotCompare(self,src_image1,src_image2):

        img1 = Image.open(src_image1)
        img2 = Image.open(src_image2)

        try:
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


    def findSubImageCordinates(self,fullscreenshot,subimage):

        '''
        This function is used to find if an image consist of subimage if yes return the co-ordinates
        :param fullscreenshot: fullpage screenshot
        :param subimage: sub-image which you want to find inside the fullpage image
        :return: list of co-ordinates(tuples with x,y co-ord) found
        '''

        #create image array for manipulation
        arr_f = np.asarray(fullscreenshot)
        arr_s = np.asarray(subimage)

        #Get the dimensions of the numpy image array
        y_f, x_f = arr_f.shape[:2]
        y_s, x_s = arr_s.shape[:2]


        xstop = x_f - x_s + 1
        ystop = y_f - y_s + 1

        matches = []

        for xmin in range(0, xstop):
            for ymin in range(0, ystop):
                xmax = xmin + x_s
                ymax = ymin + y_s

                arr_sub = arr_f[ymin:ymax, xmin:xmax]   # extract subimage
                arr_t = (arr_sub == arr_s)              # create test matrix
                if arr_t.all():                         # test whether all array elements along a given axis evaluate to True and only consider exact matches
                    matches.append((xmin, ymin))

        return matches