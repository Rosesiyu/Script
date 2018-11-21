# -- coding: utf-8 --
import datetime
import os, sys

from src.utils.Log import GetLog
from src.utils.TrainingState import TrainingState
from src.utils.Login_Logout import Login_Logout
from src.utils.AddUser import AddUser
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
from src.utils.Change_Wifi import Change_Wifi
from src.utils.SystemSetting import SystemSetting
from src.utils.ManageAccount import ManageAccount

if (len(sys.argv) < 2):
    print("Invalid parameters,please enter 1 parameter!")
    exit()

times = sys.argv[1]
# state = None
work_path = os.getcwd()
Log_path = work_path + "/output/"
Log_file = Log_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_FCT.txt"

if not os.path.exists(Log_path):
    os.mkdir(Log_path)


def doExercise():
    ConductButton().clickButton(const.btn_start)
    for x in range(1, 6):
        if x == 1:
            GetLog().log(Log_file, "Muscle Development mode!")
            ConductButton().clickButton(const.btn_MuscleDevelopment)
        if x == 2:
            GetLog().log(Log_file, "Cardiovascular mode!")
            ConductButton().clickButton(const.btn_Cardiovascular)
        if x == 3:
            GetLog().log(Log_file, "Relax mode!")
            ConductButton().clickButton(const.btn_Relax)
        if x == 4:
            GetLog().log(Log_file, "Manual Setting mode!")
            ConductButton().clickButton(const.btn_ManualSetting)
        if x == 5:
            GetLog().log(Log_file, "Professional mode!")
            ConductButton().clickButton(const.btn_Professional)
        TrainingState().Start()
        Change_Wifi().changeWifi()
        AddUser().addWirelessUser()
        TrainingState().Start()
        TrainingState().Pause()
        TrainingState().Stop()
        ConductButton().clickButton(const.btn_back)


for x in range(int(times)):
    GetLog().log(Log_file, "Round: " + str(x))
    Login_Logout().loginAdmin()
#	ManageAccount().createTrainer_User()
    SystemSetting().systemSetting()
    Login_Logout().logOut()
    Login_Logout().loginTrainer()
    AddUser().addWireUser()
    AddUser().addWirelessUser()
    doExercise()
    Login_Logout().logOut()
