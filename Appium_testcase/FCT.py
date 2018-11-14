# -- coding: utf-8 --
import datetime
import os
import sys

import init
from constant import const

if (len(sys.argv) < 2):
    print ("Invalid parameters,please enter 1 parameter!")
    exit()

times = sys.argv[1]
#state = None
work_path = os.getcwd()
Log_path = work_path  + "/output/"
Log_file = Log_path +  datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_FCT.txt"

if not os.path.exists(Log_path):
	os.mkdir(Log_path)

def Log(file,msg):
	doc = open(file,'a')
	if doc:
		logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg  + '\n'
		if file == Log_file:
			print(logmsg)
		doc.write(logmsg)
		doc.close()

def doExercise():
	init.clickButton(const.btn_start)
	for x in range(1,6):
		if x == 1:
			Log(Log_file,"Muscle Development mode!")
			init.clickButton(const.btn_MuscleDevelopment)
		if x == 2:
			Log(Log_file,"Cardiovascular mode!")
			init.clickButton(const.btn_Cardiovascular)
		if x == 3:
			Log(Log_file,"Relax mode!")
			init.clickButton(const.btn_Relax)
		if x == 4:
			Log(Log_file,"Manual Setting mode!")
			init.clickButton(const.btn_ManualSetting)
		if x == 5:
			Log(Log_file,"Professional mode!")
			init.clickButton(const.btn_Professional)
		init.Start()
		init.Change_WIFI()
		init.addWirelessUser()
		init.Start()
		init.Pause()
		init.Stop()
		init.clickButton(const.btn_back)

for x in range(int(times)):
	Log(Log_file,"Round: " + str(x))
	init.LoginAdmin()
#	init.CreateTrainer_User()
	init.SystemSetting()
	init.Logout()
	init.LoginTrainer()
	init.addWireUser()
	init.addWirelessUser()
	doExercise()
	init.Logout()
