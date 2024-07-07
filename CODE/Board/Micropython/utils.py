import ntptime, time
from machine import Pin,RTC

def sync_ntp(url = "pool.ntp.org"):
     ntptime.NTP_DELTA = 0   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
     ntptime.host = url  # 可选，ntp服务器，默认是"pool.ntp.org"
     ntptime.settime()   # 修改设备时间,到这就已经设置好了
     lc_now = time.time()+ 8*3600
     lc_now = time.localtime(lc_now)
     rtc = RTC()
     rtc.datetime((lc_now[0],lc_now[1],lc_now[2],lc_now[6],lc_now[3],lc_now[4],lc_now[5],lc_now[7]))