# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:42:07 2022

@author: Swarnameenakshi
"""
import os
import cv2
import re
import pytesseract
import spacy
from PIL import Image
from pdf2image import convert_from_path

file = 'oct 2021.pdf'

# Convert necessary pages to jpg from pdf
# Store Pdf with convert_from_path function
images = convert_from_path(file, 500, poppler_path="E:\\Anaconda\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")
#for i in range(len(images)):
images[0].save('file.jpg', 'JPEG')

# Image read from jpg
img = cv2.imread('file.jpg')
gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# threshold
gry = cv2.threshold(gry, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
f_name = "{}.png".format(os.getpid())
cv2.imwrite(f_name, gry)

# Extract text
text = pytesseract.image_to_string(Image.open(f_name), lang='eng')
#print (text)

for line in text.split('\n'):
    if "Bharat" in line:
        name_bsnl = re.search('Tax Invoice.*?PAY NOW', text, re.DOTALL).group()
        
    #if "Airtel" in line:
        #name_airtel = line.split(':')[1]
        
        
nlp = spacy.load("en_core_web_sm")
doc = nlp(name_bsnl)

print([chunk.text for chunk in doc.noun_chunks])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
       
#print (name_bsnl)
#print (name_airtel)
os.remove(f_name)

#cv2.imshow("Image", img)
#cv2.imshow("Output", gry)
#cv2.waitKey(0)