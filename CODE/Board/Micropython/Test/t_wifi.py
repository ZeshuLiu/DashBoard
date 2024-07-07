import network, time, ntptime

def sync_ntp(url = "pool.ntp.org"):
     # ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
     ntptime.host = url  # 可选，ntp服务器，默认是"pool.ntp.org"
     ntptime.settime()   # 修改设备时间,到这就已经设置好了

f = open("wifi.conf", encoding='utf-8')
ssid = f.readline()[:-2]
pwd = f.readline()[:-2]
uurl = f.readline()
print([ssid, pwd, uurl])
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("开始连接")
while not wlan.isconnected():
    wlan.connect(ssid, pwd)
    print('.', end='')

print("连接成功")
sync_ntp(uurl)
print(time.localtime())

