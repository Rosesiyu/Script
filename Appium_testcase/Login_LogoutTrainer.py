# -- coding: utf-8 --
import unittest
import time
from appium import webdriver
import sys
import urllib
from appium.webdriver.common.touch_action import TouchAction
import datetime
import os
import re

if (len(sys.argv) < 2):
    print ("Invalid parameters,please enter 1 parameters!")
    exit()

readDeviceId = list(os.popen('adb devices').readlines())
device_id = re.findall(r'^\w*\b', readDeviceId[1])[0]

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1'
desired_caps['deviceName'] = device_id
desired_caps['appPackage'] = 'fitshang.com.shaperlauncher'
desired_caps['appActivity'] =  '.mvp.ui.view.main.MainActivity'
desired_caps['noReset'] = 'true'
desired_caps['fullReset'] = 'false'
driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)  #启动app
time.sleep(10)

times = sys.argv[1]

work_path = os.getcwd()
Log_path = work_path  + "/output"
Log_file = Log_path + "/Login_LogoutTrainer.txt"

if not os.path.exists(Log_path):
	os.mkdir(Log_path)
	
def inputPW():
	driver.find_element_by_android_uiautomator('new UiSelector().text("1")').click()
	driver.find_element_by_android_uiautomator('new UiSelector().text("2")').click()
	driver.find_element_by_android_uiautomator('new UiSelector().text("3")').click()
	driver.find_element_by_android_uiautomator('new UiSelector().text("4")').click()
	time.sleep(2)

def Log(msg):
	doc = open(Log_file,'a+')
	if doc:
		logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg  + '\n'
		print(logmsg)
		doc.write(logmsg)
		doc.close()

#管理员登陆
def loginAdmin():
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_comm_btn_name").click()
	inputPW()

#创建账户
def CreateAccount(account,password):
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_tab_add").click()    #点击添加按钮
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/et_user_nickname").click()
	time.sleep(1)
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/et_user_nickname").send_keys(account)  #设置账号
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/et_tel").click()
	time.sleep(1)
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/et_tel").send_keys(password)   #设置电话
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_btn_user_create_pin").click()
	inputPW()
	time.sleep(1)
	inputPW()   #确认密码
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_btn_user_save").click()  #点击创建
	time.sleep(5)
	try:
		NickName1 = driver.find_element_by_id('fitshang.com.shaperlauncher:id/tv_item_trainer_name').text
		if NickName1 == account:
			pass
	except Exception as e:
		Log("Failed to create user")
		pass

def CreateTrainer_User():
	driver.find_element_by_android_uiautomator('new UiSelector().text("Account Setting")').click() #点击账户设置
	NickName2 = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_name").text
	if NickName2 != "Add New Account" :
		pass
	else:
		CreateAccount("aaa","34567")
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_tab_user").click()  #切换到学员添加界面
	NickName3 = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_name").text
	if NickName3 != "Add New Account" :
		pass
	else:
		CreateAccount("hhh","3456789")

def logout():
	try:
		icon = driver.find_element_by_id("fitshang.com.shaperlauncher:id/comm_btn_back")
		while icon:
			icon.click()
			try:
				confirm_ok = driver.find_element_by_id("fitshang.com.shaperlauncher:id/confirm_ok")
				if confirm_ok:
					confirm_ok.click()
			except Exception as e:
				pass
			icon = driver.find_element_by_id("fitshang.com.shaperlauncher:id/comm_btn_back")
	except Exception as e:
		pass

#教练登陆
def loginTrainer():
	driver.find_element_by_class_name("android.widget.RelativeLayout").click() 
	try:
		trainer_tel = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_tel")
		if trainer_tel:
			inputPW()
	except Exception as e:
		Log("Please add user!")
		loginAdmin()
		CreateTrainer_User()
		logout()
		loginTrainer()

#教练添加用户
def addUser():
	loginTrainer()
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_tab_add").click()  #点击添加按钮
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_manual_check").click() #选择手动添加
	try:
		user_exist = driver.find_element_by_id("fitshang.com.shaperlauncher:id/rtv_btn_user_save")
		if user_exist:
			nameB = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_name").text
			user_exist.click()
			driver.find_element_by_android_uiautomator('new UiSelector().text("Wire Mode")').click() #选择有线模式
			time.sleep(10)
			nameA = driver.find_element_by_id('fitshang.com.shaperlauncher:id/tv_item_trainer_name').text
			try:
				assert(nameA == nameB),"Failed to add user!"
			except AssertionError as msg:
				print (msg)
	except Exception as e:
		Log("Failed to get the user list!")
		driver.find_element_by_id("fitshang.com.shaperlauncher:id/confirm_ok").click()
	
#退出教练登陆
def logoutTrainer():
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/comm_btn_back").click()
	time.sleep(1)
	driver.find_element_by_id("fitshang.com.shaperlauncher:id/confirm_ok").click()
	time.sleep(10)
	try:
		loading_exist = driver.find_element_by_id("fitshang.com.shaperlauncher:id/loading")
		if loading_exist:
			Log("Failed to logout trainer!")
#			sys.exit()
	except Exception as e:
		pass
	try:
		trainer_tel = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_item_trainer_tel")
		if trainer_tel:
			Log("Logout successfully!")
	except Exception as e:
		Log("Failed to get the trainer list!")
		pw_exist = driver.find_element_by_id("fitshang.com.shaperlauncher:id/tv_psw_lable")
		if pw_exist:
			pass
		else:
			Log("The page is blank!")
		sys.exit()

if __name__=="__main__":
	for x in range(int(times)):
		addUser()
		logoutTrainer()
		Log("Times " + str(x))