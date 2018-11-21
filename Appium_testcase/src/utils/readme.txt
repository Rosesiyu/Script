from appium import webdriver

from appium.webdriver.common.touch_action import TouchAction

from src.utils.AddUser import AddUser
	clickAdd(),addWireUser(),addWirelessUser(),chooseWirelessMode()

from src.utils.Change_Wifi import Change_Wifi
	changeWifi()

from src.utils.ConductButton import ConductButton
	getButton(buttonname),clickButton(buttonname)

from src.utils.constant import const

from src.utils.InputPW import InputPW
    inputPW()

from src.utils.Log import GetLog
	log(file, msg)

from src.utils.Login_Logout import Login_Logout
	loginTrainer(),loginAdmin(),logoutTrainer(),logOut()

from src.utils.ManageAccount import ManageAccount
	createAccount(account, password),deleteAccount(),deleteAll(),createTrainer_User()

from src.utils.serport import SerialPort
	switchAdb()

from src.utils.SystemSetting import SystemSetting
	systemSetting()

from src.utils.TrainingState import TrainingState
	data_add_by_progressbar(),data_dec_by_progressbar(),get_training_state(),Start(),Pause(),Stop()

