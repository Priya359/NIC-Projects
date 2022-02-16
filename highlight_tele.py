# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 19:35:23 2022

@author: Swarnameenakshi
"""
import pytesseract 
import argparse
import cv2
 
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
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

# Dilate to combine adjacent text contours
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
dilate = cv2.dilate(thresh, kernel, iterations=4)

# Find contours, highlight text areas, and extract ROIs
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

ROI_number = 0
for c in cnts:
    area = cv2.contourArea(c)
    if area > 10000:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
        ROI = image[y:y+h, x:x+w]
        cv2.imwrite('Results/ROI_{}.png'.format(ROI_number), ROI)
        text = pytesseract.image_to_string(ROI)
        text = "".join(text).strip()
        if "Bharat" in text:
            #list_of_words = text.split()
            #next_word = list_of_words[list_of_words.index("Period") + 1]+" "+list_of_words[list_of_words.index("Period") + 2]+" "+list_of_words[list_of_words.index("Period") + 3]
            print (text)
        
        ROI_number += 1
        
#cv2.imshow('thresh', thresh)
#cv2.imshow('dilate', dilate)
#cv2.imshow('image', image)
#cv2.waitKey()
