# This file is executed on every boot (including wake-boot from deepsleep)
import esp32,time, network, ntptime
from src.usr import usr_time,Seg_Msg, Oled_Msg,NeoPixel_Msg
from machine import Pin,RTC
from utils import *
#esp.osdebug(None)
#import webrepl
#webrepl.start()

ShowTime_ms = 1000
CloseDisp = 1

f = open("wifi.conf", encoding='utf-8')
ssid = f.readline()[:-2]
pwd = f.readline()[:-2]
uurl = f.readline()
print([ssid, pwd, uurl])

# time.sleep(1)

wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(1)
wlan.active(True)
print("开始连接")
while not wlan.isconnected():
    time.sleep(4)
    wlan.connect(ssid, pwd)
    print('.', end='')

print("连接成功")
try:
    sync_ntp(uurl)
    print("同步成功")
except OSError:
    pas
print(time.localtime())

#校准系统时间
rtc = RTC()
#usr_time.Rtc2DS(dbg = False)
# usr_time.DS2Rtc(dbg = False)

# rtc.datetime( time.localtime())
print("Now RTC : ",list(rtc.datetime())[:-1])
# print("Now RTC : ",list(time.localtime())[:-1])

#显示设备显示启动信息
Seg_Msg.ShowBootMsg()
Oled_Msg.ShowBootMsg()
NeoPixel_Msg.ShowBootMsg()

ctrl = Pin(23, Pin.IN, Pin.PULL_UP)

#清除显示
if CloseDisp or ctrl.value() == 0:
    time.sleep_ms(ShowTime_ms)
    Seg_Msg.EndDisp()
    Oled_Msg.EndDisp()
    if ShowTime_ms < 500:
        time.sleep_ms(2000-ShowTime_ms)
    NeoPixel_Msg.EndDisp()
