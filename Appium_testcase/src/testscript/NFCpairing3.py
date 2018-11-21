# -- coding: utf-8 --
import threading, datetime, time, os, sys

from src.utils.Login_Logout import Login_Logout
from src.utils.AddUser import AddUser
from src.utils.serport import SerialPort
from src.utils.Log import GetLog
from src.utils.constant import const
from src.utils.ConductButton import ConductButton

if (len(sys.argv) < 2):
    print("Invalid parameters,please enter 1 parameter!")
    exit()

PairTimes = sys.argv[1]
work_path = os.getcwd()
Log_path = work_path + "/output/"
Log_file = Log_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_NFCpairing.txt"
NFClog_path = work_path + "/NFCLog/"
NFClog_file = NFClog_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_NFC.txt"

if not os.path.exists(Log_path):
    os.mkdir(Log_path)

if not os.path.exists(NFClog_path):
    os.mkdir(NFClog_path)

# 教练登陆
Login_Logout().loginTrainer()

match_state = None


def SaveLog():
    global match_state
    SerialPort.serport.write('\r$EMD9\r')
    time.sleep(1)
    SerialPort.serport.write('\r$EMD4\r')
    time.sleep(1)
    while True:
        #		if str_towrite is not None:
        #			serport.write(str_towrite)
        #			str_towrite = None
        data = SerialPort.serport.readline()
        GetLog().log(NFClog_file, repr(data))
        if match_state == True:
            break


def NFCPairing():
    n = 0
    AddUser().addWireUser()
    ConductButton().clickButton(const.btn_start)
    ConductButton().clickButton(const.btn_MuscleDevelopment)
    for x in range(int(PairTimes)):
        AddUser().clickAdd()
        while AddUser().chooseWirelessMode():
            n += 1
            GetLog().log(Log_file, "NFC Pairing failed !!! Failed counter: " + str(n))
        GetLog().log(Log_file, "NFC Pairing succeed !!! Succeed counter: " + str(x))


def thread():
    global match_state
    t1 = threading.Thread(target=SaveLog)
    t2 = threading.Thread(target=NFCPairing)
    t1.start()
    t2.start()
    t2.join()
    match_state = True
    return match_state


if __name__ == "__main__":
    thread()
#	driver.quit()
