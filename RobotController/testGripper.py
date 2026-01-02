import socket
import time

ROBOT_IP = "192.168.0.10"
PORT = 29999  # Dashboard server

def dashboard(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, PORT))
    s.recv(1024)  # welcome msg
    s.send((cmd + "\n").encode())
    resp = s.recv(1024).decode()
    s.close()
    return resp

# ---- CONTROL PROGRAM ----

print(dashboard("load rg2_pick_place.urp"))
time.sleep(1)

print(dashboard("play"))
