# -- coding: utf-8 --
import serial


class SerialPort:
    serport = serial.Serial(port='COM4', baudrate=115200, timeout=2)
    def switchAdb(self):
        global serport
        self.serport.write('\r$EEPD\r')
        self.serport.write('\r$EEPU\r')
        self.serport.write('\r$EEPP\r')
