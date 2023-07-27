import src.bsp.tm1637 as tm1637
from machine import Pin

def ShowBootMsg(tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16))):
    tm.show('-.U.P.-')

def EndDisp(tm = tm1637.TM1637Decimal(clk=Pin(4), dio=Pin(16)) ):
    #tm.show('    ')
    tm.write([0, 0, 0, 128])

if __name__ == "__main__":
    ShowBootMsg()