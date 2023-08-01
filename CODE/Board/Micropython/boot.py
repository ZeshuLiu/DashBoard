# This file is executed on every boot (including wake-boot from deepsleep)
import esp32,time
from src.usr import usr_time,Seg_Msg, Oled_Msg,NeoPixel_Msg
from machine import Pin,RTC
#esp.osdebug(None)
#import webrepl
#webrepl.start()

ShowTime_ms = 1000
CloseDisp = 1


#校准系统时间
rtc = RTC()
#usr_time.Rtc2DS(dbg = False)

usr_time.DS2Rtc(dbg = False)

#rtc.datetime( (2023, 7, 27, 3, 0, 16, 44, 0) )
print("Now RTC : ",list(rtc.datetime())[:-1])

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
