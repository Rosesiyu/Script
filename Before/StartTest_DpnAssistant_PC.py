# -*- coding: UTF-8 -*-

import os
import sys
import urllib
import urllib2
import win32com
import win32com.client
import zipfile
import shutil
import json
import codecs
    
def save_sync_file(file, data):
    with codecs.open(file, 'w', 'utf-8') as json_file:
        json_file.write(json.dumps(data, encoding = "UTF-8", ensure_ascii = False))
        json_file.close()

def exit_with_error(file, error_msg):
    with codecs.open(file, 'w', 'utf-8') as json_file:
        json_data_error = {}
        json_data_error["Status"] = 2   #2代表测试执行过程失败
        json_data_error["ErrorMsg"] = error_msg #ErrorMsg为Status等于2时的错误信息（原因），否则为空或该域不存在
        json_file.write(json.dumps(json_data_error, encoding = "UTF-8", ensure_ascii = False))
        json_file.close()
        exit()

def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar,arcname)
    zf.close()

if (len(sys.argv) < 1):
    print "Invalid parameters"
    exit()
elif(len(sys.argv) < 4):
    sync_file = sys.argv[1]
    exit_with_error(sync_file, "Invalid parameters, no sync file")

json_data = {}
json_data["Status"] = 1        #0代表测试进行中，1代表测试完成，2代表测试执行过程失败
test_results = {}              #Update test_results according to the actual results

sync_file    = sys.argv[1]
build_number = sys.argv[2]
download_url = sys.argv[3]

work_path           = os.path.dirname(os.path.abspath("StartTest_DpnAssistant_PC.py"))
download_path       = work_path + "Download/"
report_path         = work_path + "TestReport/"
uft_setup_path      = work_path + "UFT_DpnAssistantSetup/"
uft_path            = work_path + "UFT_DpnAssistant/"
setup_file_name_zip = "DpnAssistantSetup.zip"
setup_file_name     = "DpnAssistantSetup.exe"

if os.path.exists(download_path + build_number):
    exit_with_error(sync_file, "This build is already tested: " + build_number)
    
if os.path.exists(report_path + build_number):
    exit_with_error(sync_file, "This build is already tested: " + build_number)

os.chdir(work_path)
os.mkdir(download_path + build_number)
os.chdir(download_path + build_number)

try:
    urllib.urlretrieve(download_url, setup_file_name_zip)
except:
    exit_with_error(sync_file, "Failed to download file")

try:
    zfile = zipfile.ZipFile(setup_file_name_zip, 'r')
    #data = zfile.read(setup_file_name)
    data = zfile.read("DpnAssistant/" + setup_file_name)
    file = open(setup_file_name, 'w+b')
    file.write(data)
    file.close()
except:
    exit_with_error(sync_file, "Failed to unzip file")

shutil.copy (setup_file_name, uft_setup_path + setup_file_name)
os.chdir(work_path)

uft_setup_test = uft_setup_path + "Test.tsp";
os.mkdir(report_path + build_number)

try:
    QtpApp = win32com.client.Dispatch("QuickTest.Application")
    QtpApp.Launch()
    QtpApp.Visible = False
    QtpApp.Options.Run.CaptureForTestResults = "OnError"
    QtpApp.Options.Run.ImageCaptureForTestResults = "OnError"
    QtpApp.Options.Run.RunMode = "Fast"
    QtpApp.Options.Run.ViewResults = False
    QtpApp.Open(uft_setup_test)
    QtpResult = win32com.client.Dispatch("QuickTest.RunResultsOptions")
    QtpResult.ResultsLocation = report_path + build_number
    QtpApp.Test.Run(QtpResult)
except:
    exit_with_error(sync_file, "Failed to run " + uft_setup_path + "Test.tsp")

if (QtpApp.Test.LastRunResults.Status == "Passed"):
    test_results["安装测试"] = 1    #0代表失败，1代表成功，2代表忽略（未执行）
else:
    test_results["安装测试"] = 0    #0代表失败，1代表成功，2代表忽略（未执行）

QtpApp.Test.Close()
QtpApp.Quit()

try:
    zip_dir(report_path + build_number, report_path + build_number + '.zip')
except:
    exit_with_error(sync_file, "Failed to zip report")

test_results["功能测试"] = 2

json_data["Results"] = test_results
json_data["ReportFile"] = report_path + build_number + '.zip'

save_sync_file(sync_file, json_data);