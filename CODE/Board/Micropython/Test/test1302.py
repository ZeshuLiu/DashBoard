from machine import Pin,RTC
import src.bsp.ds1302 as ds1302

ds = ds1302.DS1302(clk=Pin(18),dio=Pin(5),cs=Pin(17))
rtc = RTC()

ds.date_time() # returns the current datetime.
print(ds.date_time())
ds.date_time(list(rtc.datetime())) # set datetime.

ds.hour() # returns hour.
print(ds.date_time())

print()

print(rtc.datetime())
ds.second(10) # set second to 10.