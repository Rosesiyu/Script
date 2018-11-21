# -- coding: utf-8 --
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
import time


class Change_Wifi:
    def changeWifi(self):
        ConductButton.clickButton(const.btn_top_wifi)
        try:
            self.wifi_id = ConductButton.getButton(const.btn_wifi_input).text
            ConductButton.clickButton(const.btn_input_clear)
            if self.wifi_id == "SFBVB-PSXR3-SFB2X-OOGGA":
                print("Connect S3000000")
                ConductButton.getButton(const.btn_wifi_input).send_keys("SFVUI-HCXR3-SFB2X-OOGGA")
                ConductButton.clickButton(const.btn_Network_ID)
            else:
                print("Connect S1000000")
                ConductButton.getButton(const.btn_wifi_input).send_keys("SFBVB-PSXR3-SFB2X-OOGGA")
                ConductButton.clickButton(const.btn_Network_ID)
            time.sleep(5)
        except:
            pass
        try:
            self.wifi_state = ConductButton.getButton(const.btn_wifi_Connected)
            if self.wifi_state:
                self.wifi_state.click()
                time.sleep(1)
                ConductButton.clickButton(const.btn_confirm_ok)
        except:
            pass
        ConductButton.clickButton(const.btn_wifi_Connect)
        time.sleep(30)
        try:
            self.wifi_state2 = ConductButton.getButton(const.btn_wifi_Connected)
            if self.wifi_state2:
                ConductButton.clickButton(const.btn_back)
            else:
                ConductButton.clickButton(const.btn_wifi_Connect)
                time.sleep(30)
                ConductButton.clickButton(const.btn_back)
        except:
            pass