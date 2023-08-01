from src.usr import usr_time,Seg_Msg, Oled_Msg,NeoPixel_Msg
from machine import Pin,RTC
import time, dht
from CONFIG import *

defaultMode = 0

class ButtonStat:
    def __init__(self) -> None:
        self.LongPress_ms = 1500

        self.ENC1 = 0
        self.ENC2 = 0
        self.CtrButton = 0
        self.BotButtonShort = 0
        self.BotButtonLong = 0
    
    def reset(self):
        self.ENC1 = 0
        self.ENC2 = 0
        self.CtrButton = 0
        self.BotButtonShort = 0
        self.BotButtonLong = 0

class MainWorking:
    def __init__(self, BStat:ButtonStat, modeIndex=0, cdt=45) -> None:
        self.ModeIndex = modeIndex
        self.ModeOldIndex = modeIndex
        self.ModeDisp = 0
        self.ModeDispStart_ms = 0;
        self.MaxMode = 3

        self.BStat = BStat

        self.rtc = RTC()

        self.dht11 = dht.DHT11(Pin(32))
        
        self.CountDownTime_min = cdt
        self.CountDownStart_ms = 0
        self.IFCountDown = 0
        self.NotExceed = 1
        pass
    
    def SingleWork(self):
        if self.ModeIndex == 0:
            self.Mode1()


        elif self.ModeIndex == 1:
            self.Fun1()

        elif self.ModeIndex == 2:
            self.Fun2()

        elif self.ModeIndex == 3:
            self.Fun3()
        else:
            self.ModeIndex = defaultMode
        
        if self.ModeOldIndex != self.ModeIndex:
            self.ModeDisp = 1
            self.ModeDispStart_ms = time.ticks_ms()
            self.ModeOldIndex = self.ModeIndex
            Seg_Msg.EndDisp()
            Oled_Msg.EndDisp()
            NeoPixel_Msg.EndDisp()
        
        if self.ModeDisp:
            if time.ticks_ms() - self.ModeDispStart_ms < ModeChangeDispTime_ms:
                Seg_Msg.NumberDisp(self.ModeIndex)
            else:
                Seg_Msg.EndDisp()
                self.ModeDisp = 0


        self.BStat.reset()

    def Mode1(self):
        """
        Neo 显示时间——模拟表盘
        Oled显示: 1. 温湿度
        Seg显示: 休息倒计时,倒计时结束后
        """
        #print("NeoTimeDisp")
        if self.NotExceed:
            NeoPixel_Msg.NeoTimeDisp(list(self.rtc.datetime())[:-1])
        
        if time.ticks_ms() % DHT11MesureGap_ms < MainWorkGap*2:
            self.dht11.measure()
            t = self.dht11.temperature() 
            h = self.dht11.humidity() 
            Oled_Msg.Show_Temp_Hum_Date(t,h, list(self.rtc.datetime())[:-1])
            print("Showing Temp",t,h)
            #Oled_Msg.Show_date(list(self.rtc.datetime())[:-1])

        if not self.IFCountDown:
            Seg_Msg.NumberDisp(self.CountDownTime_min)
            if self.BStat.BotButtonShort == 1:
                self.CountDownStart_ms = time.ticks_ms()
                self.IFCountDown = 1
                self.NotExceed = 1
                with open('./dat/CountDownTime.txt', 'w') as CDT:
                    CDT.write(str(self.CountDownTime_min))
                CDT.close()
                print("Write Count Down Time to File, Time = ", self.CountDownTime_min)

        else:
            left = self.CountDownTime_min - int((time.ticks_ms() - self.CountDownStart_ms)/(60*1000))
            #print(left)
            #print(self.CountDownStart_ms)
            #print(time.ticks_ms())
            if left >= 0:
                Seg_Msg.NumberDotDisp('0'*(4-len(str(left)))+str(left)+'.')
            else:
                if self.NotExceed == 1:
                    Seg_Msg.NumberDotDisp('-.-.-.-.')
                    NeoPixel_Msg.ShowBootMsg()
                    self.NotExceed = 0
                

            if self.BStat.BotButtonLong == 1:
                self.IFCountDown = 0
                self.NotExceed = 1



        if (not self.IFCountDown) and self.BStat.ENC2 != 0:
            if self.BStat.ENC2 < 0:
                self.CountDownTime_min += self.BStat.ENC2
                if self.CountDownTime_min < 0:
                    self.CountDownTime_min += 9999
            else:
                self.CountDownTime_min += self.BStat.ENC2
                if self.CountDownTime_min > 9999:
                    self.CountDownTime_min -= 9999

        self.Enc1_default()

    def Fun1(self):
        print("Func1")
        if self.BStat.ENC1 != 0:
            if self.BStat.ENC1 < 0:
                if self.ModeIndex!=0:
                    self.ModeIndex -= 1
                else:
                    self.ModeIndex = self.MaxMode
            else:
                if self.ModeIndex!=self.MaxMode:
                    self.ModeIndex += 1
                else:
                    self.ModeIndex = 0

    def Fun2(self):
        print("Func2")

        if self.BStat.ENC1 != 0:
            if self.BStat.ENC1 < 0:
                if self.ModeIndex!=0:
                    self.ModeIndex -= 1
                else:
                    self.ModeIndex = self.MaxMode
            else:
                if self.ModeIndex!=self.MaxMode:
                    self.ModeIndex += 1
                else:
                    self.ModeIndex = 0

    def Fun3(self):
        print("Func3")

        if self.BStat.ENC1 != 0:
            if self.BStat.ENC1 < 0:
                if self.ModeIndex!=0:
                    self.ModeIndex -= 1
                else:
                    self.ModeIndex = self.MaxMode
            else:
                if self.ModeIndex!=self.MaxMode:
                    self.ModeIndex += 1
                else:
                    self.ModeIndex = 0

    def Enc1_default(self):
        if self.BStat.ENC1 != 0:
            if self.BStat.ENC1 < 0:
                if self.ModeIndex!=0:
                    self.ModeIndex -= 1
                else:
                    self.ModeIndex = self.MaxMode
            else:
                if self.ModeIndex!=self.MaxMode:
                    self.ModeIndex += 1
                else:
                    self.ModeIndex = 0
