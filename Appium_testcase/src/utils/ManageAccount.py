# -- coding: utf-8 --
import time
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
from src.utils.Login_Logout import Login_Logout


class ManageAccount:
    # 创建账户
    def createAccount(self, account, password):
        self.account = account
        self.password = password
        ConductButton.clickButton(const.btn_tab_add)  # 点击添加按钮
        ConductButton.clickButton(const.btn_user_nickname)
        ConductButton.getButton(const.btn_user_nickname).send_keys(self.account)  # 设置账号
        ConductButton.clickButton(const.btn_et_tel)
        ConductButton.getButton(const.btn_et_tel).send_keys(self.password)  # 设置电话
        ConductButton.clickButton(const.btn_user_create_pin)
        Login_Logout.inputPW()
        time.sleep(1)
        Login_Logout.inputPW()  # 确认密码
        ConductButton.clickButton(const.btn_user_save)  # 点击创建
        time.sleep(5)
        try:
            self.nickname1 = ConductButton.getButton(const.btn_trainer_name).text
            if self.nickname1 == self.account:
                print("Create " + account + " successfully!")
        except Exception as e:
            print("Failed to create user!")
            pass

    # 删除学员
    def deleteAccount(self):
        self.tel1 = ConductButton.getButton(const.btn_trainer_name).text
        ConductButton.clickButton(const.btn_user_detail_edit)
        ConductButton.clickButton(const.btn_user_delete)
        ConductButton.clickButton(const.btn_confirm_ok)
        time.sleep(5)
        try:
            self.tel2 = ConductButton.getButton(const.btn_trainer_tel).text
            if self.tel2 and self.tel2 == self.tel1:
                print("Failed to deleteAccount!")
        except Exception as e:
            print("deleteAccount successfully!")
            pass

    # 删除所有学员
    def deleteAll(self):
        self.nickname2 = ConductButton.getButton(const.btn_trainer_name).text
        while self.nickname2 != "Add New Account":
            self.deleteAccount()
            self.nickname2 = ConductButton.getButton(const.btn_trainer_name).text

    # 创建账户
    def createTrainer_User(self):
        ConductButton.clickButton(const.btn_AccountSetting)  # 点击账户设置
        self.nickname2 = ConductButton.getButton(const.btn_trainer_name).text
        if self.nickname2 != "Add New Account":
            self.deleteAll()
            print("Delete all the trainers!")
        self.createAccount("Maggie", "13652456845")
        self.createAccount("Kitty", "18245623578")
        self.createAccount("Cici", "15254623548")
        self.createAccount("Lom", "13145688615")
        ConductButton.clickButton(const.btn_tab_user)  # 切换到学员添加界面
        time.sleep(3)
        self.nickname3 = ConductButton.getButton(const.btn_trainer_name).text
        if self.nickname3 != "Add New Account":
            self.deleteAll()
            print("Delete all the users!")
        self.createAccount("Jeff", "15245879523")
        self.createAccount("Aimi", "18245796583")
        self.createAccount("Tomas", "15212548565")
        self.createAccount("Bane", "15245898745")
        ConductButton.clickButton(const.btn_back)