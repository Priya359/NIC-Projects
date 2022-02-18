# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 11:06:02 2022

@author: Swarnameenakshi
"""
import pytesseract 
import cv2
from pdf2image import convert_from_path

file = 'oct 2021.pdf'
operator = input ("Enter the operator name: ")

if operator == "BSNL": 
    m=30
    n=30
elif operator == "Airtel":
    m=30
    n=20
elif operator == "Jio":
    m=40
    n=20
    
images = convert_from_path(file, 500, poppler_path="E:\\Anaconda\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")
images[0].save('read_file.jpg', 'JPEG')

image = cv2.imread('read_file.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (m,n))
dilate = cv2.dilate(thresh, kernel, iterations=4)

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
        text = "".join(text).strip('\nt')
        #print (text)
        
        for line in text.split('\n'):
                if operator == "Airtel":
                    if "eriod" in line:
                        per = line[line.index("eriod") + len("eriod"):].replace(' ','').split(":")
                        print(per)
                    if "MISS"  in line:
                        nam = line[line.index("MISS") + len("MISS"):].replace(' ','').split(":")
                        print(nam)
                    if "Amount Due" in line:
                        amt = line[line.index("Due") + len("Due"):].replace(' ','').split(":")
                        print(amt)
                    elif "Total @" in line:
                        amt = line[line.index("@") + len("@"):].replace(' ','').split("\t")
                        print(amt)
                    if  "Airtel number" in line:
                        num = line[line.index("number") + len("number"):].replace(' ','').split(":")
                        print(num)
                    elif "Phone Number" in line:
                        num = line[line.index("Number") + len("Number"):].replace(' ','').split(":")
                        print(num)
                    if "Statement Date" in line:
                        dat = line[line.index("Date") + len("Date"):].replace(' ','').split(":")
                        print(dat)
                    elif "Bill date" in line:
                        dat = line[line.index("date") + len("date"):].replace(' ','').split(":")
                        print(dat)
                        
                if operator == "BSNL":
                    if "AMOUNT PAYABLE" in text:
                        print(line)
                    if "TELEPHONE NUMBER" in text:
                        print(line)
                    if "Invoice Date" in text:
                        print(line)
                    if "Billing Period" in text:
                        print(line)
                    
                    
                        
                        
        ROI_number += 1        
   
