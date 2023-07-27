from machine import Pin,RTC
import src.bsp.ds1302 as ds1302


def Rtc2DS( ds= ds1302.DS1302(clk=Pin(18),dio=Pin(5),cs=Pin(17)), rtc = RTC(), dbg=True):
    
    # 打印当前存储的时间
    if dbg:
        print("DS Time Before Saving:",",".join( [str(i) for i in ds.date_time()] ) )
    
    # 打印要存储的时间
    Time2Save = list(rtc.datetime())[:-1]
    if dbg:
        print("Time to Save:",",".join( [str(i) for i in Time2Save] ))
    
    #存储时间
    ds.date_time(Time2Save) 
    
    #打印存储的时间
    if dbg:
        print("DS Time After Saving:",",".join( [str(i) for i in ds.date_time()] ))

def DS2Rtc (ds= ds1302.DS1302(clk=Pin(18),dio=Pin(5),cs=Pin(17)), rtc = RTC(), dbg=True):
    
    # 打印当前RTC的时间
    if dbg:
        print("RTC Time Before Saving:",",".join( [ str(i) for i in list(rtc.datetime())[:-1] ] ) )
    
    # 打印要存储的时间
    Time2Save = list(ds.date_time()) + [0]
    if dbg:
        print("Time to Save:",",".join( [str(i) for i in Time2Save] ))
    
    #存储时间
    rtc.datetime(Time2Save) 
    
    #打印存储的时间
    if dbg:
        print("Time After Saving:",",".join( [ str(i) for i in list(rtc.datetime())[:-1] ] ))

if __name__ == "__main__":
    Rtc2DS()
    DS2Rtc()