# -- coding: utf-8 --
import os,sys

from src.utils.constant import const
from src.utils.Log import GetLog
from src.utils.ConductButton import ConductButton
from src.utils.Login_Logout import Login_Logout
from src.utils.ManageAccount import ManageAccount

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


# 管理员登陆
Login_Logout.loginAdmin()
ConductButton.clickButton(const.btn_AccountSetting)  # 点击账户设置

if __name__ == "__main__":
    for m in range(int(number1)):
        GetLog.log(Log_file, "counter: " + str(m))
        ManageAccount.deleteAll()
        GetLog.log(Log_file, "Delete all the trainers!")
        ManageAccount.createAccount("Maggie", "13652456845")
        ManageAccount.createAccount("Kitty", "18245623578")
        ManageAccount.createAccount("Cici", "15254623548")
        ManageAccount.createAccount("Tom", "13145684615")
        m += 1
    ConductButton.clickButton(const.btn_tab_user)  # 切换到学员添加界面
    NickName3 = ConductButton.getButton(const.btn_trainer_name).text
    for n in range(int(number2)):
        GetLog.log(Log_file, "counter: " + str(n))
        ManageAccount.deleteAll()
        GetLog.log(Log_file, "Delete all the users!")
        ManageAccount.createAccount("Jeff", "15245879523")
        ManageAccount.createAccount("Jimi", "18245796583")
        ManageAccount.createAccount("Tomas", "15212548565")
        ManageAccount.createAccount("Jane", "15245898745")
        n += 1
