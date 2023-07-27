# This file is executed on every boot (including wake-boot from deepsleep)
import esp32,time
from src.usr import usr_time,Seg_Msg, Oled_Msg,NeoPixel_Msg
from machine import Pin,RTC
#esp.osdebug(None)
#import webrepl
#webrepl.start()

ShowTime_ms = 3000
CloseDisp = 0


#校准系统时间
usr_time.DS2Rtc(dbg = False)
rtc = RTC()
print("Now RTC : ",list(rtc.datetime())[:-1])

#显示设备显示启动信息
Seg_Msg.ShowBootMsg()
Oled_Msg.ShowBootMsg()
NeoPixel_Msg.ShowBootMsg()

#清除显示
if CloseDisp:
    time.sleep_ms(ShowTime_ms)
    Seg_Msg.EndDisp()
    Oled_Msg.EndDisp()
    if ShowTime_ms < 2000:
        time.sleep_ms(2000-ShowTime_ms)
    NeoPixel_Msg.EndDisp()
