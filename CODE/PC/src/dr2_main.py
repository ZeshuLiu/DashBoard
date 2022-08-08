#import psutil
import time
import dr2_udp
import socket
import numpy





# Testing
if __name__ == '__main__':
    while True:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_addr = ("127.0.0.1", 50777)
        udp_socket.bind(local_addr)
        np,_ = dr2_udp.receive(udp_socket)
        print(np)
        print(np[0])
        time.sleep(2)
