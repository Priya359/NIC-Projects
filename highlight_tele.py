# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 19:35:23 2022

@author: Swarnameenakshi
"""
import pytesseract 
import argparse
import cv2
from pytesseract import Output
 
# We construct the argument parser
# and parse the arguments
ap = argparse.ArgumentParser()
 
ap.add_argument("-i", "--image",
                required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-c", "--min-conf",
                type=int, default=0,
                help="minimum confidence value to filter weak text detection")
args = vars(ap.parse_args())
 
# We load the input image and then convert
# it to RGB from BGR. We then use Tesseract
# to localize each area of text in the input
# image
images = cv2.imread(args["image"])
(h, w, c) = images.shape[:3]
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
 
# Then loop over each of the individual text
# localizations
for i in range(0, len(results["text"])):
     
    # We can then extract the bounding box coordinates
    # of the text region from  the current result
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]
     
    # We will also extract the OCR text itself along
    # with the confidence of the text localization
    text = results["text"][i]
    conf = int(float(results["conf"][i]))
     
    # filter out weak confidence text localizations
    if conf > args["min_conf"]:
         
        # We will display the text to
        # our terminal
        t1 = str(x) +"+"+ str(y)
        t2 = str(x+w) +"+"+ str(y+h)
        coor = t1+","+t2
        
        #print("Confidence: {}".format(conf))
        #print("Text: {}".format(text))
        #print("")
         
        # We then strip out non-ASCII text so we can
        # draw the text on the image We will be using
        # OpenCV, then draw a bounding box around the
        # text along with the text itself
        text = "".join(text).strip()
        cv2.rectangle(images,
                      (x, y),
                      (x + w, y + h),
                      (0, 0, 255), 2)
        cv2.putText(images,
                    coor,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2, (0, 255, 255), 3)

        print (text)
# After all, we will show the output image
cv2.imwrite("newimage.jpg", images)
cv2.imshow("Image", images)
cv2.waitKey(0)

#num2words.num2words(123456, lang='en_IN')
