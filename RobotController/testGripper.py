import socket
import time

ROBOT_IP = "192.168.1.10"   # CHANGE THIS
PORT = 30002               # URScript port

def send_urscript(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ROBOT_IP, PORT))
    s.send((cmd + "\n").encode())
    s.close()

# ---- TEST RG2 ----

print("Opening gripper")
send_urscript("RG2(60,40,0.0,True,False,False)")
time.sleep(2)

print("Closing gripper")
send_urscript("RG2(10,40,0.0,True,False,False)")
time.sleep(2)

print("Done")
