from machine import Pin,RTC
import time, dht

d = dht.DHT11(Pin(32))
d.measure()  # 先调用测量函数
t = d.temperature()  # 温度
h = d.humidity()  # 湿度

print("temperature:",t,"℃")
print("humidity:",h,"%")
