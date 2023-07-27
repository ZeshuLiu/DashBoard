from src.usr import usr_time,Seg_Msg, Oled_Msg,NeoPixel_Msg
from machine import Pin,RTC

defaultMode = 0

class ButtonStat:
    def __init__(self) -> None:
        self.ENC1 = 0
        self.ENC2 = 0
        self.CtrButton = 0
        self.BotButton = 0
    
    def reset(self):
        self.ENC1 = 0
        self.ENC2 = 0
        self.CtrButton = 0
        self.BotButton = 0

class MainWorking:
    def __init__(self, BStat:ButtonStat, modeIndex=0) -> None:
        self.ModeIndex = modeIndex
        self.MaxMode = 3
        self.BStat = BStat
        self.rtc = RTC()
        pass
    
    def SingleWork(self):
        if self.ModeIndex == 0:
            self.NeoTimeDisp()


        elif self.ModeIndex == 1:
            self.Fun1()

        elif self.ModeIndex == 2:
            self.Fun2()

        elif self.ModeIndex == 3:
            self.Fun3()
        else:
            self.ModeIndex = defaultMode
        
        self.BStat.reset()

    def NeoTimeDisp(self):
        #print("NeoTimeDisp")
        NeoPixel_Msg.NeoTimeDisp(list(self.rtc.datetime())[:-1])
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

