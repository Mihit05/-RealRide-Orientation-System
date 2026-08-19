import socket
import math

HOST = "10.182.162.148"  # ESP32 IP (printed in serial)
PORT = 1234

s = socket.socket()
s.connect((HOST, PORT))

while True:
    data = s.recv(1024).decode().strip()
    
    try:
        ax, ay, az, gx, gy, gz = map(int, data.split(","))
        print("Acc: {ax, ay, az} | Gyro: {gx, gy, gz}")
    except:
        pass
    def accel_to_angle(ax, ay, az):
        roll = math.atan2(ay, az)
        pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2))
        return roll, pitch
    