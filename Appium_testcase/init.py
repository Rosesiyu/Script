# -- coding: utf-8 --
import os
import re
import sys
import time

import serial
from appium import webdriver

from constant import const

readDeviceId = list(os.popen('adb devices').readlines())
device_id = re.findall(r'^\w*\b', readDeviceId[1])[0]

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1'
desired_caps['deviceName'] = 'device_id'
desired_caps['appPackage'] = 'fitshang.com.shaperlauncher'
desired_caps['appActivity'] =  '.mvp.ui.view.main.MainActivity'
desired_caps['automationName'] = 'uiautomator2'
driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)	#启动app
time.sleep(20)

match_state = None
str_towrite = None
state = None
serport = serial.Serial(port='COM4', baudrate=115200, timeout=2)
if serport is None:
	print("SwitchAdb: Can't find the serial port!")

def getButton(ButtonName):
	if "id/" in ButtonName: 
		return driver.find_element_by_id(ButtonName)
	elif "new UiSelector()" in ButtonName:
		return driver.find_element_by_android_uiautomator(ButtonName)
	else:
		return driver.find_element_by_class_name(ButtonName)

def clickButton(ButtonName):
	Button = getButton(ButtonName)
	if Button:
		Button.click()
		time.sleep(2)

#教练登陆
def LoginTrainer():
	clickButton(const.btn_RelativeLayout)
	try:
		Button = getButton(const.btn_trainer_tel)
		if Button:
			inputPW()
			time.sleep(5)
	except Exception as e:
		print ('Please add user!')
		LoginAdmin()
		CreateTrainer_User()
		Logout()
		LoginTrainer()

def clickAdd():
	try:
		clickButton(const.btn_add_user)
	except:
		clickButton(const.btn_tab_add)
	try:
		while getButton(const.btn_manual_add):
			getButton(const.btn_manual_add).click()
	except Exception as e:
		pass
	clickButton(const.btn_user_save)
#教练添加有线模式学员
def addWireUser():
	clickAdd()
	clickButton(const.btn_wire_mode) #选择有线模式
	time.sleep(8)
#教练添加无线模式学员
def addWirelessUser():
	time.sleep(2)
	clickAdd()
	clickButton(const.btn_wireless_mode) #选择无线模式
	SwitchAdb()
	print ("Pairing!!!")
	time.sleep(40)
	print ("End of match")
	result = None
	n = 0
	try:
		result = getButton(const.btn_wireless_mode)
		while result:
			n += 1
			print ("NFC Pairing failed !!! Failed counter: " + str(n))
			result.click() #选择无线模式
			SwitchAdb()
			print ("Pairing!!!")
			time.sleep(40)
			print ("End of match")
			result = getButton(const.btn_wireless_mode)
	except Exception as e:
		print ("NFC Pairing succeed !!!")

def inputPW():
	clickButton(const.btn_one)
	clickButton(const.btn_two)
	clickButton(const.btn_three)
	clickButton(const.btn_four)
#退出教练登陆
def LogoutTrainer():
	clickButton(const.btn_back)
	clickButton(const.btn_confirm_ok)
	time.sleep(10)
	try:
		loading_exist = getButton(const.btn_loading)
		if loading_exist:
			print ("Failed to logout trainer!")
			sys.exit()
	except Exception as e:
		pass
	try:
		trainer_tel = getButton(const.btn_trainer_tel)
		if trainer_tel:
			print ("Logout successfully!")
	except Exception as e:
		print ("Failed to get the trainer list!")
		pw_exist = getButton(const.btn_psw_lable)
		if not pw_exist:
			print ("The page is blank!")
		sys.exit()

def SwitchAdb():
	serport.write(b'\r$EEPD\r')
	serport.write(b'\r$EEPU\r')
	serport.write(b'\r$EEPP\r') 
	print ("In pairing state !")

def chooseWirelessMode():
	clickButton(const.btn_wireless_mode) #选择无线模式
	SwitchAdb()
	print ("Pairing!!!")
	time.sleep(45)
	print ("End of match")
	result = None
	try:
		result = getButton(const.btn_wireless_mode)
		time.sleep(5)
		if result:
			result = True
	except Exception as e:
		result = False
	return result

def Change_WIFI():
	clickButton(const.btn_top_wifi)
	try:
		wifi_id = getButton(const.btn_wifi_input).text
		clickButton(const.btn_input_clear)
		if wifi_id == "SFBVB-PSXR3-SFB2X-OOGGA":
			print ("Connect S3000000")
			getButton(const.btn_wifi_input).send_keys("SFVUI-HCXR3-SFB2X-OOGGA")
			clickButton(const.btn_Network_ID)
		else:
			print ("Connect S1000000")
			getButton(const.btn_wifi_input).send_keys("SFBVB-PSXR3-SFB2X-OOGGA")
			clickButton(const.btn_Network_ID)
		time.sleep(5)
	except:
		pass
	try:
		wifi_state = getButton(const.btn_wifi_Connected)
		if wifi_state:
			wifi_state.click()
			time.sleep(1)
			clickButton(const.btn_confirm_ok)
	except:
		pass
	clickButton(const.btn_wifi_Connect)
	time.sleep(30)
	try:
		wifi_state2 = getButton(const.btn_wifi_Connected)
		if wifi_state2:	
			clickButton(const.btn_back)
		else:
			clickButton(const.btn_wifi_Connect)
			time.sleep(30)
			clickButton(const.btn_back)
	except:
		pass

def data_add_by_progressbar():
	for x in range(0,3):
		try:
			progress_bar = getButton(const.btn_progress_bar)
			if progress_bar: 
				driver.swipe(560, 853, 1300, 853, 1)
		except Exception as e:
			time.sleep(1)
			pass
		x += 1
	time.sleep(2)

def data_dec_by_progressbar():
	for x in range(0,3):
		try:
			progress_bar = getButton(const.btn_progress_bar)
			if progress_bar: 
				driver.swipe(1300, 853, 560, 853, 1)
		except Exception as e:
			time.sleep(1)
			pass
		x += 1
	time.sleep(2)

def get_training_state():
	global state
	try:
		Button = getButton(const.btn_name).text
		if Button:
			state = "Stopped"
	except Exception as e:
		pass
	try:
		start_time = getButton(const.btn_tainer_time_small).text
		if start_time :
			state = "Started"
	except Exception as e:
		pass
	try:
		pause_text = getButton(const.btn_pasue_text).text
		if(pause_text == 'Paused') :
			state = "Paused"
	except Exception as e:
		pass
	return state

def Start():
	global state
	clickButton(const.btn_start)   #开始运动
	time.sleep(2)
	state = get_training_state()
	if(state != 'Started'):
		print ("Failed to start")
		clickButton(const.btn_start)
	else:
		print ("Started successfully!")
	time.sleep(7)
	try:
		progress_bar = getButton(const.btn_progress_bar)
		if not progress_bar:
			clickButton(const.btn_master)
	except Exception as e:
		pass
	data_add_by_progressbar()
	data_dec_by_progressbar()
	data_add_by_progressbar()
	clickButton(const.btn_abdomen)
	data_add_by_progressbar()
	data_dec_by_progressbar()
	data_add_by_progressbar()

def Pause():
	global state
	clickButton(const.btn_start)   #暂停运动
	time.sleep(2)
	state = get_training_state()
	if(state != "Paused"):
		print ("Failed to pause")
#		clickButton(const.btn_start)
	else:
		print ("Paused successfully!")
	time.sleep(7)

def Stop():
	global state
	clickButton(const.btn_back)   #停止运动
	time.sleep(2)
	state = get_training_state()
	if(state != "Stopped"):
		print ("Failed to stop")
#		clickButton(const.btn_back)
	else:
		print ("Stopped successfully!")
	time.sleep(7)


#管理员登陆
def LoginAdmin():
	clickButton(const.btn_admin)
	inputPW()
#创建账户
def CreateAccount(account,password):
	clickButton(const.btn_tab_add)    #点击添加按钮
	clickButton(const.btn_user_nickname)
	getButton(const.btn_user_nickname).send_keys(account)  #设置账号
	clickButton(const.btn_et_tel)
	getButton(const.btn_et_tel).send_keys(password)   #设置电话
	clickButton(const.btn_user_create_pin)
	inputPW()
	time.sleep(1)
	inputPW()   #确认密码
	clickButton(const.btn_user_save)  #点击创建
	time.sleep(5)
	try:
		NickName1 = getButton(const.btn_trainer_name).text
		if NickName1 == account:
			print ("Create " + account + " successfully!")
	except Exception as e:
		print ("Failed to create user!")
		pass
#删除学员
def DeleteAccount():
	tel1 = getButton(const.btn_trainer_name).text
	clickButton(const.btn_user_detail_edit)
	clickButton(const.btn_user_delete)
	clickButton(const.btn_confirm_ok)
	time.sleep(5)
	try:
		tel2 = getButton(const.btn_trainer_tel).text
		if tel2 and tel2 == tel1:
			print ("Failed to deleteAccount!")
	except Exception as e:
		print ("DeleteAccount successfully!")
		pass
#删除所有学员
def DeleteAll():
	NickName2 = getButton(const.btn_trainer_name).text
	while NickName2 != "Add New Account" :
		DeleteAccount()
		NickName2 = getButton(const.btn_trainer_name).text
#创建账户
def CreateTrainer_User():
	clickButton(const.btn_AccountSetting) #点击账户设置
	NickName2 = getButton(const.btn_trainer_name).text
	if NickName2 != "Add New Account" :
		DeleteAll()
		print ("Delete all the trainers!")
	CreateAccount("Maggie","13652456845")
	CreateAccount("Kitty","18245623578")
	CreateAccount("Cici","15254623548")
	CreateAccount("Lom","13145688615")
	clickButton(const.btn_tab_user)  #切换到学员添加界面
	time.sleep(3)
	NickName3 = getButton(const.btn_trainer_name).text
	if NickName3 != "Add New Account" :
		DeleteAll()
		print ("Delete all the users!")
	CreateAccount("Jeff","15245879523")
	CreateAccount("Aimi","18245796583")
	CreateAccount("Tomas","15212548565")
	CreateAccount("Bane","15245898745")
	clickButton(const.btn_back)
#系统设置
def SystemSetting():
	clickButton(const.btn_SystemSetting)
	time.sleep(3)
	try:
		display_btn = getButton(const.btn_name).text
		if display_btn == "Display":
			clickButton(const.btn_display)
	except Exception as e:
		print (u"系统设置界面异常")
		clickButton(const.btn_back)
		clickButton(const.btn_SystemSetting)
	finally:
		clickButton(const.btn_display)
		print ("Enter the display interface")
		clickButton(const.btn_back)
		clickButton(const.btn_restore)
		print ("Enter the restore interface")
		clickButton(const.btn_confirm_cancel)
		clickButton(const.btn_DateTime)
		print ("Enter the datetime interface")
		clickButton(const.btn_back)
		clickButton(const.btn_Language)
		time.sleep(2)
		print ("Enter the language interface")
		clickButton(const.btn_confirm_cancel)
#登出
def Logout():
	try:
		icon = getButton(const.btn_back)
		while icon:
			icon.click()
			time.sleep(2)
			try:
				clickButton(const.btn_confirm_ok)
			except Exception as e:
				pass
			icon = getButton(const.btn_back)
	except Exception as e:
		pass