# -- coding: utf-8 --
import unittest
import time
import datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import sys
import urllib
import os
import re
import serial
import threading
import ctypes
import init
from init import serport
from constant import const

if (len(sys.argv) < 2):
    print ("Invalid parameters,please enter 1 parameter!")
    exit()

PairTimes = sys.argv[1]
work_path = os.getcwd()
Log_path = work_path  + "/output/"
Log_file = Log_path +  datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_NFCpairing.txt"
NFClog_path = work_path  + "/NFCLog/"
NFClog_file = NFClog_path +  datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_NFC.txt"

if not os.path.exists(Log_path):
	os.mkdir(Log_path)

if not os.path.exists(NFClog_path):
	os.mkdir(NFClog_path)

def Log(file,msg):
	doc = open(file,'a')
	if doc:
		logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg  + '\n'
		if file == Log_file:
			print(logmsg)
		doc.write(logmsg)
		doc.close()

#教练登陆
init.LoginTrainer()

match_state = None
def SaveLog():
	global match_state
	serport.write('\r$EMD9\r')
	time.sleep(1)
	serport.write('\r$EMD4\r')
	time.sleep(1)
	while True:
#		if str_towrite is not None:
#			serport.write(str_towrite)
#			str_towrite = None
		data = serport.readline()
		Log(NFClog_file,repr(data))
		if match_state == True:
			break

def NFCPairing():
	n = 0
	init.addWireUser()
	init.clickButton(const.btn_start)
	init.clickButton(const.btn_MuscleDevelopment)
	for x in range(int(PairTimes)):
		init.clickAdd()
		while init.chooseWirelessMode():
			n += 1
			Log(Log_file,"NFC Pairing failed !!! Failed counter: " + str(n))
		Log(Log_file,"NFC Pairing succeed !!! Succeed counter: " + str(x))

def thread():
	global match_state
	t1 = threading.Thread(target= SaveLog)
	t2 = threading.Thread(target= NFCPairing)
	t1.start()
	t2.start()
	t2.join()
	match_state = True
	return match_state

if __name__=="__main__":
	thread()
#	driver.quit()
