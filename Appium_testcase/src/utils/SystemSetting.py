# -- coding: utf-8 --
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
import time

class SystemSetting:
    # 系统设置
    def systemSetting(self):
        ConductButton().clickButton(const.btn_SystemSetting)
        time.sleep(3)
        try:
            self.display_btn = ConductButton().getButton(const.btn_name).text
            if self.display_btn == "Display":
                ConductButton().clickButton(const.btn_display)
        except Exception as e:
            print(u"系统设置界面异常")
            ConductButton().clickButton(const.btn_back)
            ConductButton().clickButton(const.btn_SystemSetting)
        finally:
            ConductButton().clickButton(const.btn_display)
            print("Enter the display interface")
            ConductButton().clickButton(const.btn_back)
            ConductButton().clickButton(const.btn_restore)
            print("Enter the restore interface")
            ConductButton().clickButton(const.btn_confirm_cancel)
            ConductButton().clickButton(const.btn_DateTime)
            print("Enter the datetime interface")
            ConductButton().clickButton(const.btn_back)
            ConductButton().clickButton(const.btn_Language)
            time.sleep(2)
            print("Enter the language interface")
            ConductButton().clickButton(const.btn_confirm_cancel)