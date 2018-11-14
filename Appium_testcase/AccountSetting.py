# -- coding: utf-8 --
import datetime
import os
import sys

import init
from constant import const

if len(sys.argv) < 3:
    print("Invalid parameters,please enter 2 parameters!")
    exit()

number1 = sys.argv[1]
number2 = sys.argv[2]

work_path = os.getcwd()
Log_path = work_path + "/output"
Log_file = Log_path + "/AccountSetting.txt"

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


# 管理员登陆
init.LoginAdmin()
init.clickButton(const.btn_AccountSetting)  # 点击账户设置

if __name__ == "__main__":
    for m in range(int(number1)):
        Log(Log_file, "counter: " + str(m))
        init.DeleteAll()
        Log(Log_file, "Delete all the trainers!")
        init.CreateAccount("Maggie", "13652456845")
        init.CreateAccount("Kitty", "18245623578")
        init.CreateAccount("Cici", "15254623548")
        init.CreateAccount("Tom", "13145684615")
        m += 1
    init.clickButton(const.btn_tab_user)  # 切换到学员添加界面
    NickName3 = init.getButton(const.btn_trainer_name).text
    for n in range(int(number2)):
        Log(Log_file, "counter: " + str(n))
        init.DeleteAll()
        Log(Log_file, "Delete all the users!")
        init.CreateAccount("Jeff", "15245879523")
        init.CreateAccount("Jimi", "18245796583")
        init.CreateAccount("Tomas", "15212548565")
        init.CreateAccount("Jane", "15245898745")
        n += 1
