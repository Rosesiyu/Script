@echo off
set  MYPWD=E:\script\results
echo %time% >> %MYPWD%\Time.txt

:loop
::adb shell cat /sys/devices/virtual/thermal/thermal_zone0/temp >> %MYPWD%\CPU0_Temp.txt
adb shell cat /sys/devices/virtual/thermal/thermal_zone1/temp >> %MYPWD%\CPU_Temp.txt
adb shell cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq >> %MYPWD%\cpu0_freq.txt
adb shell cat /sys/devices/system/cpu/cpu1/cpufreq/scaling_cur_freq >> %MYPWD%\cpu1_freq.txt
adb shell cat /sys/devices/system/cpu/cpu2/cpufreq/scaling_cur_freq >> %MYPWD%\cpu2_freq.txt
adb shell cat /sys/devices/system/cpu/cpu3/cpufreq/scaling_cur_freq >> %MYPWD%\cpu3_freq.txt
adb shell cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq >> %MYPWD%\cpu4_freq.txt
adb shell cat /sys/devices/system/cpu/cpu5/cpufreq/scaling_cur_freq >> %MYPWD%\cpu5_freq.txt
adb shell cat /sys/class/devfreq/ff9a0000.gpu/cur_freq >> %MYPWD%\GPU_freq.txt
::adb shell dumpsys meminfo fitshang.com.shaperlauncher >> %MYPWD%\meminfo.txt
::adb shell top | find "fitshang.com.shaperlauncher" >> %MYPWD%\cpuinfo.txt
ping /n 1 /w 1 9.9.9.9 1>nul 2>nul
goto loop
pause
