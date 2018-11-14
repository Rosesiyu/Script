# -- coding: utf-8 --
import datetime
import os
import sys

import init

if len(sys.argv) < 3:
    print("Invalid parameters,please enter 3 parameters!")
    exit()

number1 = sys.argv[1]
number2 = sys.argv[2]
work_path = os.getcwd()
Log_path = work_path + "/output"
Log_file = Log_path + "/Doingexercise_wiremode.txt"

if not os.path.exists(Log_path):
    os.mkdir(Log_path)


def Log(file, msg):
    doc = open(file, 'a')
    if doc:
        logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg + '\n'
        if file == Log_file:
            print(logmsg)
        doc.write(logmsg)
        doc.close()


init.LoginTrainer()
init.addWireUser()


def Start_Pause():
    init.Start()
    for m in range(int(number1)):
        Log(Log_file, "pause counter: " + str(m))
        init.Pause()
        init.Start()


def Start_Stop():
    for n in range(int(number2)):
        Log(Log_file, "stop counter: " + str(n))
        init.Stop()
        init.Start()


if __name__ == "__main__":
    Start_Pause()
    Start_Stop()
# driver.quit()
