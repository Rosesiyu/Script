# -- coding: utf-8 --
import time,re,os
from appium import webdriver

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