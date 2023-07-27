from machine import Pin,RTC
from CONFIG import *
import esp32,time
from src.usr.WorkingMode import MainWorking, ButtonStat


#引脚状态存储
Buttons = ButtonStat()

#回调函数
#编码器1
Enc1_Debounce = time.ticks_ms()
def Enc1CallBack(pin):
    global Enc1_Debounce
    # 0,0逆时针; 0，1顺时针
    t0 = time.ticks_ms()
    if t0 - Enc1_Debounce > DebonuceTime:
        print("Enc1:", Enc1A.value(), ",", Enc1B.value())
        if Enc1B.value():
            Buttons.ENC1+=1
        else:
            Buttons.ENC1-=1
        Enc1_Debounce = t0

#编码器2
Enc2_Debounce = time.ticks_ms()
def Enc2CallBack(pin):
    global Enc2_Debounce
    # 0,0逆时针; 0，1顺时针
    t0 = time.ticks_ms()
    if t0 - Enc2_Debounce > DebonuceTime:
        print("Enc2:", Enc2A.value(), ",", Enc2B.value())
        if Enc2B.value():
            Buttons.ENC2+=1
        else:
            Buttons.ENC2-=1
        Enc2_Debounce = t0

#初始化引脚
ctrl = Pin(CTRL_PIN, Pin.IN, Pin.PULL_UP)
boot = Pin(BOOT_PIN, Pin.IN, Pin.PULL_UP)
Enc1A = Pin(ENC1A_PIN, Pin.IN, Pin.PULL_UP)
Enc1B = Pin(ENC1B_PIN, Pin.IN, Pin.PULL_UP)
Enc2A = Pin(ENC2A_PIN, Pin.IN, Pin.PULL_UP)
Enc2B = Pin(ENC2B_PIN, Pin.IN, Pin.PULL_UP)

Enc1A.irq(trigger=Pin.IRQ_FALLING, handler=Enc1CallBack)
Enc2A.irq(trigger=Pin.IRQ_FALLING, handler=Enc2CallBack)

#功能列表
MWorking = MainWorking(Buttons)

while True: 
    time.sleep_ms(100)
    MWorking.SingleWork()

    if ctrl.value() == 0:
        break


