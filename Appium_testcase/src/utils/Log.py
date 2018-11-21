# -- coding: utf-8 --
import datetime


class GetLog:
    def log(self,file, msg):
        self.file = file
        self.msg = msg
        self.doc = open(file, 'a')
        if self.doc:
            self.logmsg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + msg + '\n'
            self.doc.write(self.logmsg)
            self.doc.close()