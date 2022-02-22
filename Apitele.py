# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:42:07 2022

@author: Swarnameenakshi
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import cv2
import pytesseract
from pdf2image import convert_from_path

file = '9021387282_SDCTN0057331491.pdf'
app = Flask(__name__)
api = Api(app)

class HealthCheck(Resource):

	def get(self):
		return jsonify({'health': 'OK'})


class BillPdfReader(Resource):

	def get(self):
		query_parameters = request.args
		billName = query_parameters.get('billName')
		operatorName = query_parameters.get('operatorName')

		if 'Airtel' == operatorName:
			response = self.airtel_bill(billName)
		elif 'BSNL' == operatorName:
			response = self.bsnl_bill(billName)
		elif 'Vodafone' == operatorName:
			response = self.vodafone_bill(billName)
		elif 'Jio' == operatorName:
			response = self.jio_bill(billName)

		print(response)
		return response


# write function of each operator like this and return json with these values
def airtel_bill(self, bill):
    images = convert_from_path(bill, 500, poppler_path="E:\\Anaconda\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")
    images[0].save('read_file.jpg', 'JPEG')

    image = cv2.imread('read_file.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,20))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if cnts:
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
                
                for line in text.split('\n'):
                    nam = ["MR","MISS","MRS","MS","Mr","Miss","Mrs","Ms"]
                    for i in nam:
                        if i in line:
                            names = line[line.index(i) + len(i):].replace(' ',' ').split(":")
                            name = names[len(names)-1]
                    if "eriod" in line:
                        bill_periods = line[line.index("eriod") + len("eriod"):].replace(' ','').split(":")
                        bill_period = bill_periods[len(bill_periods)-1]
                    if "Amount Due" in line:
                        bill_amounts = line[line.index("Due") + len("Due"):].replace(' ','').split(":")
                        bill_amount = bill_amounts[len(bill_amounts)-1]
                    elif "Total @" in line:
                          bill_amounts = line[line.index("@") + len("@"):].replace(' ','').split("\t")
                          bill_amount = bill_amounts[len(bill_amounts)-1]
                    if  "Airtel number" in line:
                         mobile_numbers = line[line.index("number") + len("number"):].replace(' ','').split(":")
                         mobile_number = mobile_numbers[len(mobile_numbers)-1]
                    elif "Mobile" in line:
                          mobile_numbers = line[line.index("Mobile") + len("Mobile"):].split(" ", 2)
                          mobile_number = mobile_numbers[len(mobile_numbers)-2]
                    if "Statement Date" in line:
                        bill_dates = line[line.index("Date") + len("Date"):].replace(' ','').split(":")
                        bill_date = bill_dates[len(bill_dates)-1]
                    elif "Bill date" in line:
                          bill_dates = line[line.index("date") + len("date"):].replace(' ','').split(":")
                          bill_date = bill_dates[len(bill_dates)-1]
                

            ROI_number += 1       

        return jsonify({
				'Name': name,
				'Mobile_number': mobile_number,
				'Bill_period': bill_period,
				'Total_amount': bill_amount,
				'Bill_date': bill_date})
    
    else:
        return jsonify({'Error': 'Image not clear. Please upload a clear image.'})

def bsnl_bill(self, bill):
    images = convert_from_path(bill, 500, poppler_path="E:\\Anaconda\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")
    images[0].save('read_file.jpg', 'JPEG')

    image = cv2.imread('read_file.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if cnts:
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
                
                if "AMOUNT PAYABLE" in text:
                    w = text.split()
                    bill_amount = w[w.index("PAYABLE") + 2]
                if "TELEPHONE NUMBER" in text:
                    w = text.split()
                    mobile_number = w[w.index("NUMBER") + 1]
                    #print(phn)
                    ROI = image[632:1088,119:963] 	#Name of the person is matched using the coordinates of the bounding box over it
                    text = pytesseract.image_to_string(ROI)
                    if text:
                        name = text.split('\n', 1)[0]
                        #print(name)
                if "Invoice Date" in text:
                    w = text.split()
                    bill_date = w[w.index("Date") + 2]
                    #print(dat)
                if "Billing Period" in text:
                    w = text.split()
                    bill_period = w[w.index("Period") + 1]+" "+w[w.index("Period") + 2]+" "+w[w.index("Period") + 3]
                    #print(bill_per)
                

            ROI_number += 1       

        return jsonify({
				'Name': name,
				'Mobile_number': mobile_number,
				'Bill_period': bill_period,
				'Total_amount': bill_amount,
				'Bill_date': bill_date})
        
    else:
        return jsonify({'Error': 'Image not clear. Please upload a clear image.'})
        
        
def jio_bill(self, bill):
    images = convert_from_path(bill, 500, poppler_path="E:\\Anaconda\\poppler-0.68.0_x86\\poppler-0.68.0\\bin")
    images[0].save('read_file.jpg', 'JPEG')

    image = cv2.imread('read_file.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9,9), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if cnts:
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
                
                for line in text.split('\n'):
                   names = ["MR","MISS","MRS","MS","Mr","Miss","Mrs","Ms"]
                   for i in names:
                       if i in line:
                           nam = line[line.index(i) + len(i):].replace(' ',' ').split(".")
                           name = nam[len(nam)-1]
                           
                   if "Statement Date" in line:
                      bill_dates = line[line.index("Date") + len("Date"):].replace(' ','').split(":")
                      bill_date = bill_dates[len(bill_dates)-1]
                     
                   if "Jio Number" in line:
                      mobile_numbers = line[line.index("Number") + len("Number"):].replace(' ','').split(":")
                      mobile_number = mobile_numbers[len(mobile_numbers)-1]
                      
                if "Pay By" in text:
                    w = text.split()
                    bill_amounts = w[w.index("By") + 3].split("-")
                    bill_amount = bill_amounts[len(bill_amounts)-1]
                    
                if "Statement from" in text:
                    w = text.split()
                    bill_periods = w[w.index("from") + 1]+" "+w[w.index("from") + 2]+" "+w[w.index("from") + 3]
                    bill_period = bill_periods
                

            ROI_number += 1       

        return jsonify({
				'Name': name,
				'Mobile_number': mobile_number,
				'Bill_period': bill_period,
				'Total_amount': bill_amount,
				'Bill_date': bill_date})
    
    else:
        return jsonify({'Error': 'Image not clear. Please upload a clear image.'})


api.add_resource(BillPdfReader, '/api/v1/getBillReader')
api.add_resource(HealthCheck, '/api/v1/billReader/health')

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0')
