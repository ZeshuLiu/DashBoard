from machine import Pin, RTC, Timer
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

Boot_Debounce = time.ticks_ms()
Boot_Press_Start = time.ticks_ms()

def BootRCallBack(pin):
    global Boot_Debounce, Boot_Press_Start
    t0 = time.ticks_ms()
    if t0 - Boot_Debounce < DebonuceTime:
        return

    print("Released, dur:",t0 - Boot_Press_Start, "?",t0 - Boot_Press_Start > Buttons.LongPress_ms)
    if t0 - Boot_Press_Start > Buttons.LongPress_ms:
        print("Long Press")
        Buttons.BotButtonLong = 1
        Buttons.BotButtonShort = 0
    else:
        print("Short Press")
        Buttons.BotButtonShort = 1
        Buttons.BotButtonLong = 0

    Boot_Debounce = t0
    Boot_Press_Start = t0
    boot.irq(trigger=Pin.IRQ_FALLING , handler=BootFCallBack)

def BootFCallBack(pin):
    global Boot_Debounce, Boot_Press_Start
    t0 = time.ticks_ms()
    if t0 - Boot_Debounce < DebonuceTime:
        return
    
    print("Boot Button Pressed")
    Boot_Debounce = t0
    Boot_Press_Start = t0
    boot.irq(trigger=Pin.IRQ_RISING , handler=BootRCallBack)


#初始化引脚
ctrl = Pin(CTRL_PIN, Pin.IN, Pin.PULL_UP)
boot = Pin(BOOT_PIN, Pin.IN, Pin.PULL_UP)
Enc1A = Pin(ENC1A_PIN, Pin.IN, Pin.PULL_UP)
Enc1B = Pin(ENC1B_PIN, Pin.IN, Pin.PULL_UP)
Enc2A = Pin(ENC2A_PIN, Pin.IN, Pin.PULL_UP)
Enc2B = Pin(ENC2B_PIN, Pin.IN, Pin.PULL_UP)

Enc1A.irq(trigger=Pin.IRQ_FALLING, handler=Enc1CallBack)
Enc2A.irq(trigger=Pin.IRQ_FALLING, handler=Enc2CallBack)
boot.irq(trigger=Pin.IRQ_FALLING , handler=BootFCallBack)

#功能列表
with open('./dat/CountDownTime.txt', 'r+') as CDT:
    CDTL = CDT.readlines() # Magic number
    if CDTL == []:
        CDT.write('45')
        ct = 45
    else:
        ct = int(CDTL[0])
CDT.close()
print("Count Down Time = ", ct)
MWorking = MainWorking(Buttons,cdt= ct)

while True: 
    time.sleep_ms(MainWorkGap)
    MWorking.SingleWork()

    if ctrl.value() == 0:
        break


