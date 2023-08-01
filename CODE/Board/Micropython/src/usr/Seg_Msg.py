import src.bsp.tm1637 as tm1637
from CONFIG import *
from machine import Pin

def ShowBootMsg(tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16))):
    tm.brightness(SEG_Bright)
    tm.show('-.U.P.-')

def EndDisp( tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16)) ):
    #tm.show('    ')
    #tm.write([0, 0, 0, 128])
    tm.write([0, 0, 0, 0])

def NumberDisp( Mode:int, tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16)) ):
    tm.number(Mode)

def NumberDotDisp( NUM:str, tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16)) ):
    tm.show(NUM)
    

if __name__ == "__main__":
    ShowBootMsg()