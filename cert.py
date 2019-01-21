import re
import os
import sys
import csv
from bs4 import BeautifulSoup
from urllib.request import *
import urllib
import zipfile    
import pymysql
import progressbar
import time
import pickle
from datetime import datetime


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): #progress bar function
	formatStr = "{0:." + str(decimals) + "f}" 
	percent = formatStr.format(100 * (iteration / float(total))) 
	filledLength = int(round(barLength * iteration / float(total))) 
	bar = '#' * filledLength + '-' * (barLength - filledLength) 
	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)), 
	if iteration == total: 
		sys.stdout.write('\n') 
	sys.stdout.flush() 



def filedownload(): #file download function
	url = 'http://fl0ckfl0ck.work/cert/'
	#soup = BeautifulSoup(urlopen(url), 'html.parser') #get web source
	#ip_regex = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',str(soup)) #search ip from source
	#ip_regex = list(set(ip_regex)) #delete duplication
	#pickle.dump(ip_regex, open('ip.dump', 'wb')) #create ip dump
	ip_regex = pickle.load(open('ip.dump', 'rb')) #load ip dump
	#date_regex = re.findall("([0-9]{4}\\-[0-9]{2}\\-[0-9]{2} [0-9]{2}\\:[0-9]{2})", str(soup)) #search date from source
	#pickle.dump(date_regex, open('date.dump', 'wb'))  #create date dump
	date_regex = pickle.load(open('date.dump', 'rb')) #load date dump
	cnt = 0
	
	try:
		os.mkdir('./cert') #create cert directory
	except:
		pass
	
	print("File Download Start") #file download start
	length = len(ip_regex) #calculate length


	for i in ip_regex: #for loop
		if os.path.isfile('./cert/' + i + '.zip'): #check the files
			pass
		else:
			try:
				urlretrieve('http://fl0ckfl0ck.work/cert/' + i + '.zip', './cert/' + i + '.zip') #download file
				
				cnt += 1 #count add
				printProgress(cnt, length, "", str(cnt) + "/" + str(length),1, 50) #progress bar

			except urllib.error.URLError: #URL error check
				pass
	print("File Download Finished") #file download finish 


def unzip(): #unzip and extract csv
	if os.path.isdir('./cert'): #find cert directory
		start_time = time.time() #start time
		with open('dbinsert.csv','w', newline = '') as csv_file: #csv write
			logWriter = csv.writer(csv_file) #create writer
			dic = {} #create dictionary
			infolist = [] #create infolist
			cnt = 1 #create cnt
			print("CSV Write Start") #csv write start
			for i in os.listdir('./cert'): #for loop
				if i.endswith('.zip'): #check zip file
					zfile = zipfile.ZipFile('./cert/' + i)
					for f in zfile.infolist():
						z = zfile.open(f) #open zip
						content = z.read().decode('cp949') #read zip
						t = list(f.date_time)
						upload_date = str(datetime(*map(int, t)))
						infolist.append(upload_date) #date
						infolist.append(content.split('()')[0].replace('cn=','')) #name
						infolist.append(content.split('ou=')[1].replace(',','')) #bank
						infolist.append(content.split(',')[0].split(')')[1]) #account
						infolist.append(i.replace('.zip', '')) #ip
						infolist.append(content.split('c=')[1]) #country
						logWriter.writerow(infolist) #csv write
						del infolist[:] #array initialize
				else:
					print("File is not found") #error check
					pass
			elapsed_time = time.time() - start_time #time calculate
			print("Elapsed Time is " + str(elapsed_time) + "\nCSV Write Finished") #csv finished
	else:
		print("There are no directory or files") #if no directory or files in cert directory


if __name__ == "__main__": #main function
	choice = input("1. Download zip file \n2. Unzip and extract info to csv file \n3. Download and Unzip \nSelect argument : ")	 #check argument
	try:
		choice = int(choice) #choice check
	except:
		print("Input Error! Put the proper value") #error check
	
	if choice == 1: 
		filedownload()
	elif choice == 2:
		unzip()
	elif choice == 3:
		filedownload()
		unzip()
	else:
		print("Input Error! Put the proper value") #error check	
		