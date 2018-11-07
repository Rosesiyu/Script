# -- coding: utf-8 --
import pywinusb.hid as hid
import usb
import usb.core
import serial
import unittest
import time
import datetime
import struct

import binascii
import ctypes
import sys
import urllib
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import re
import os

logfile = "./output/testlog_" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".txt"
driver = 0
readDeviceId = list(os.popen('adb devices').readlines())
device_id = re.findall(r'^\w*\b', readDeviceId[1])[0]

if (len(sys.argv) < 1):
    print "Invalid parameters,please enter 1 parameters!"
    exit()

times_poweron_off = sys.argv[1]

def Init():
	global driver
	
	desired_caps = {}
	desired_caps['platformName'] = 'Android'
	desired_caps['platformVersion'] = '7.1'
	desired_caps['deviceName'] = 'device_id'
	desired_caps['appPackage'] = 'fitshang.com.shaperlauncher'
	desired_caps['appActivity'] = '.mvp.ui.view.main.MainActivity'
	desired_caps['automationName'] = 'uiautomator2'
	driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)	#启动app
	time.sleep(10)

	wifi_connected = False
	while not wifi_connected:
		try:
			while True:
				connect_btn = driver.find_element_by_id('fitshang.com.shaperlauncher:id/tv_connect_wifi')
				if connect_btn: 
					connect_btn.click()	
					Log("WIFI connecting")
					break
		except Exception as e:
			pass

		for x in range(int(18)):
			try:
				Login_page = driver.find_element_by_class_name("android.widget.RelativeLayout")
				if Login_page: 
					driver.find_element_by_class_name("android.widget.RelativeLayout").click()	
					driver.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
					driver.find_element_by_android_uiautomator('new UiSelector().text("2")').click()
					driver.find_element_by_android_uiautomator('new UiSelector().text("3")').click()
					driver.find_element_by_android_uiautomator('new UiSelector().text("4")').click()
					wifi_connected = True
					break;
				else:
					Log("Waiting for WIFI connect")
					time.sleep(5)
			except Exception as e:
				Log("Waiting for WIFI connect")
				time.sleep(5)
				pass
			x += 1;
	
	time.sleep(5)
	#教练添加用户
	Log("Add user!!!")
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_tab_add").click()  #点击添加按钮
	time.sleep(2)
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_manual_check").click() #选择手动添加
	time.sleep(5)
	nameB = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_name").text
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_btn_user_save").click() #点击OK
	driver.find_element_by_android_uiautomator('new UiSelector().text("Wire Mode")').click() #选择有线模式
	time.sleep(5)
	nameA = driver.find_element_by_id('fitshang.com.shaperlauncher:id/tv_item_trainer_name').text
	try:
		assert(nameA == nameB),"Failed to add user!"
	except AssertionError,msg:
		Log(msg)
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_btn_start").click()
	#driver.find_element_by_class_name("android.widget.RelativeLayout").click()
	driver.find_element_by_android_uiautomator('new UiSelector().text("Muscle Development")').click()
#	Log("Close asp mode")
#	try:	
#		time.sleep(5)
#		asp_btn = driver.find_element_by_id('fitshang.com.shaperlauncher:id/comm_btn_asp')
#		if asp_btn: 
#			asp_btn.click()		
#			driver.find_element_by_id('fitshang.com.shaperlauncher:id/confirm_ok').click()
#	except Exception as e:
#		Log("failed to close asp mode")
#		pass

def Log(msg):
	doc = open(logfile, "a")
	if doc:
		logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg  + '\r\n'
		print(logmsg)
		doc.write(logmsg)
		doc.close()

def get_training_stat():
	try:
		Button = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_comm_btn_name").text
		if (Button == "Back"):
			stat = "Stopped"
	except Exception as e:
		pass
	try:
		start_time = driver.find_element_by_id("fitshang.com.shaperlauncher:id/rl_trainer_start_time")
		if start_time :
			stat = "Started"
	except Exception as e:
		pass
	try:
		pause_text = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_pasue_text").text
		if(pause_text == 'Paused') :
			stat = "Paused"
	except Exception as e:
		pass
	Log("Now the state is " + stat)
	return stat

def sendUsbCommand(data):
	#hid.core.show_hids(target_vid = 0x0483, target_pid = 0x5770, output = sys.stdout)
	while len(data) < 50 :
		data.append(0)	
	cmd_success = False;
	all_devices = hid.HidDeviceFilter(vendor_id = 0x0483, product_id = 0x5770).get_devices()
	if not all_devices:
		Log("Can't find USB device")
	else:
		# search for our target usage
		for device in all_devices:
			try:
				device.open()
				# browse feature reports
				for report in device.find_output_reports() + device.find_feature_reports():
					# print("report id 0x%x report_type %s write data(%s): %s" % (report.report_id, report.report_type, type(data[0]), str(data)))
					if (data[0] == report.report_id):
						#print("report id 0x%x len %d" % (report.report_id, len(data)))
						cmd_success = report.send(data)
						break
			finally:
				device.close()
	
	return cmd_success
	
def SwitchAdb2():
	serport = serial.Serial(port='COM11', baudrate=1500000, timeout=2)
	if(serport is None):
		Log("SwitchAdb: Can't find the serial port!")
		return;
	serport.write("\r\nsu\r\n")
	time.sleep(5)
	serport.write("\r\necho 2 > /sys/kernel/debug/usb@fe800000/rk_usb_force_mode\r\n")
	serport.close()
	
def SwitchAdb():
	ret = sendUsbCommand([110, 0, 0, 0, 0, 11, 1])
	return ret
	
def CheckAdb():
	ret = False
	#dev =	usb.core.find(idVendor=0x2207, idProduct=0x0011)
	dev = usb.core.find(idVendor=0x483, idProduct=0x5770)
	if dev is None:
		Log("ADB not found!")
	else:
		Log("ADB found!")
		ret = True	  
	return ret

def Poweron(en):
	ret = False
	if en:
		ret = sendUsbCommand([110, 0, 0, 0, 0, 1, 1])
		if ret :
			Log('Power on')
		else :
			Log('Power on failed')
	else :
		ret = sendUsbCommand([110, 0, 0, 0, 0, 1, 0])
		if ret :
			Log('Power off')
		else :
			Log('Power off failed')

	return ret

def TestMain():
	Log("Start test total %s times" % (times_poweron_off))
	n = 0
	if times_poweron_off > 0:
		for m in range(int(times_poweron_off)):
			Poweron(False)
			time.sleep(5)
			Poweron(True)
			time.sleep(50)
			SwitchAdb()
			time.sleep(5)
			Init()
			time.sleep(5)
			Log("Start doing exercise!!!")
			driver.find_element_by_id('fitshang.com.shaperlauncher:id/rtv_btn_start').click()   #开始运动
			time.sleep(8)
			stat = get_training_stat()
			if(stat != 'Started'):
				n += 1
				Log("Connect USB failed counter: " + str(n))
			Log("Test counter: " + str(m))
			m += 1
	Log("Test end")
TestMain()

