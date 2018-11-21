# -- coding: utf-8 --
import os,datetime,sys

from src.utils.Log import GetLog
from src.utils.TrainingState import TrainingState
from src.utils.Login_Logout import Login_Logout
from src.utils.AddUser import AddUser

if len(sys.argv) < 3:
    print("Invalid parameters,please enter 3 parameters!")
    exit()

number1 = sys.argv[1]
number2 = sys.argv[2]
work_path = os.getcwd()
Log_path = work_path + "/output"
Log_file = Log_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') +"/Doingexercise_wiremode.txt"

if not os.path.exists(Log_path):
    os.mkdir(Log_path)

Login_Logout.loginTrainer()
AddUser.addWireUser()


def Start_Pause():
    TrainingState.Start()
    for m in range(int(number1)):
        GetLog.log(Log_file, "pause counter: " + str(m))
        TrainingState.Pause()
        TrainingState.Start()


def Start_Stop():
    for n in range(int(number2)):
        GetLog.log(Log_file, "stop counter: " + str(n))
        TrainingState.Stop()
        TrainingState.Start()

if __name__ == "__main__":
    Start_Pause()
    Start_Stop()
# driver.quit()
