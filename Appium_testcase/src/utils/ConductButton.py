# -- coding: utf-8 --
from main import driver
import time


class ConductButton:
    def getButton(self,buttonname):
        self.buttonname = buttonname
        if "id/" in self.buttonname:
            return driver.find_element_by_id(buttonname)
        elif "new UiSelector()" in self.buttonname:
            return driver.find_element_by_android_uiautomator(buttonname)
        else:
            return driver.find_element_by_class_name(buttonname)

    def clickButton(self,buttonname):
        self.button = self.getButton(buttonname)
        if self.button:
            self.button.click()
            time.sleep(2)