# -- coding: utf-8 --
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
from src.utils.serport import SerialPort
import time

class AddUser:
    def clickAdd(self):
        try:
            ConductButton().clickButton(const.btn_add_user)
        except:
            ConductButton().clickButton(const.btn_tab_add)
        try:
            while ConductButton().getButton(const.btn_manual_add):
                ConductButton().getButton(const.btn_manual_add).click()
        except Exception as e:
            pass
        ConductButton().clickButton(const.btn_user_save)

    # 教练添加有线模式学员
    def addWireUser(self):
        self.clickAdd()
        ConductButton().clickButton(const.btn_wire_mode)  # 选择有线模式
        time.sleep(8)

    # 教练添加无线模式学员
    def addWirelessUser(self):
        time.sleep(2)
        self.clickAdd()
        ConductButton().clickButton(const.btn_wireless_mode)  # 选择无线模式
        SerialPort().switchAdb()
        print("Pairing!!!")
        time.sleep(40)
        print("End of match")
        self.result = None
        n = 0
        try:
            self.result = ConductButton().getButton(const.btn_wireless_mode)
            while self.result:
                n += 1
                print("NFC Pairing failed !!! Failed counter: " + str(n))
                self.result.click()  # 选择无线模式
                SerialPort().switchAdb()
                print("Pairing!!!")
                time.sleep(40)
                print("End of match")
                self.result = ConductButton().getButton(const.btn_wireless_mode)
        except Exception as e:
            print("NFC Pairing succeed !!!")

    def chooseWirelessMode(self):
        ConductButton().clickButton(const.btn_wireless_mode)  # 选择无线模式
        SerialPort().switchAdb()
        print("Pairing!!!")
        time.sleep(45)
        print("End of match")
        self.result = None
        try:
            self.result = ConductButton().getButton(const.btn_wireless_mode)
            time.sleep(5)
            if self.result:
                self.result = True
        except Exception as e:
            self.result = False
        return self.result