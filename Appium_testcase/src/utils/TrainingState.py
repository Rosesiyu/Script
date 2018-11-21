# -- coding: utf-8 --
from src.utils.ConductButton import ConductButton
from src.utils.constant import const
from main import driver
import time

class TrainingState:
    state = None

    def data_add_by_progressbar(self):
        for x in range(0, 3):
            try:
                self.progress_bar = ConductButton.getButton(const.btn_progress_bar)
                if self.progress_bar:
                    driver.swipe(560, 853, 1300, 853, 1)
            except Exception as e:
                time.sleep(1)
                pass
            x += 1
        time.sleep(2)

    def data_dec_by_progressbar(self):
        for x in range(0, 3):
            try:
                self.progress_bar = ConductButton.getButton(const.btn_progress_bar)
                if self.progress_bar:
                    driver.swipe(1300, 853, 560, 853, 1)
            except Exception as e:
                time.sleep(1)
                pass
            x += 1
        time.sleep(2)

    def get_training_state(self):
        global state
        try:
            self.Button = ConductButton.getButton(const.btn_name).text
            if self.Button:
                state = "Stopped"
        except Exception as e:
            pass
        try:
            self.start_time = ConductButton.getButton(const.btn_tainer_time_small).text
            if self.start_time:
                self.state = "Started"
        except Exception as e:
            pass
        try:
            self.pause_text = ConductButton.getButton(const.btn_pasue_text).text
            if self.pause_text == 'Paused':
                state = "Paused"
        except Exception as e:
            pass
        return state

    def Start(self):
        global state
        ConductButton.clickButton(const.btn_start)  # 开始运动
        time.sleep(2)
        self.state = self.get_training_state()
        if self.state != 'Started':
            print("Failed to start")
            ConductButton.clickButton(const.btn_start)
        else:
            print("Started successfully!")
        time.sleep(7)
        try:
            self.progress_bar = ConductButton.getButton(const.btn_progress_bar)
            if not self.progress_bar:
                ConductButton.clickButton(const.btn_master)
        except Exception as e:
            pass
        self.data_add_by_progressbar()
        self.data_dec_by_progressbar()
        self.data_add_by_progressbar()
        ConductButton.clickButton(const.btn_abdomen)
        self.data_add_by_progressbar()
        self.data_dec_by_progressbar()
        self.data_add_by_progressbar()

    def Pause(self):
        global state
        ConductButton.clickButton(const.btn_start)  # 暂停运动
        time.sleep(2)
        self.state = self.get_training_state()
        if self.state != "Paused":
            print("Failed to pause")
        #		clickButton(const.btn_start)
        else:
            print("Paused successfully!")
        time.sleep(7)

    def Stop(self):
        global state
        ConductButton.clickButton(const.btn_back)  # 停止运动
        time.sleep(2)
        self.state = self.get_training_state()
        if self.state != "Stopped":
            print("Failed to stop")
        #		clickButton(const.btn_back)
        else:
            print("Stopped successfully!")
        time.sleep(7)