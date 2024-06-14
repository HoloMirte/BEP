
import socket
import serial
import time
from mirte_robot import robot
from mirte_msgs.msg import Encoder
mirte = robot.createRobot()

mirte.setMotorSpeed('mech1left', 80)
time.sleep(1)
mirte.setMotorSpeed('mech1left', 0)

#import rospy
#enc1 = 0
#enc2 = 0

#def cb1(data):
#	print(data)
#   global enc1
#   enc1 = data.value

#def cb2(data):
#	print(data)
#   global enc2
#   enc2 = data.value

#rospy.Subscriber("/mirte/encoder/mech1right", Encoder, cb1)
#rospy.Subscriber("/mirte/encoder/mech1left", Encoder, cb2)
#rospy.Subscriber("/mirte/encoder/mech2right", Encoder, cb)
#rospy.Subscriber("/mirte/encoder/mech2left", Encoder, cb)


# Setup the server socket to receive data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))  # Bind to all interfaces
server_socket.listen(1)
print("Server listening on port 65432")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")
target_min = -100
target_max = 100
input_min = -57.7350-2.5980
input_max = 57.7350+2.5980

try:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        test = message.split(",")

        x_raw = test[0].split(":")[1]
        y_raw = test[1].split(":")[1]
        z_raw = test[2].split(":")[1]

        x = float(x_raw)
        y = float(y_raw)
        z = float(z_raw)

        if abs(x)< 0.04:
            x = 0
        if abs(y)< 0.04:
            y = 0
        if abs(z)< 0.04:
            z = 0

        mech1right =-57.7350*x+33.3333*2*y-6.0621*15*z
        mech1left =57.7350*x+33.3333*2*y+6.0621*15*z
        mech2right =57.7350*x+-33.3333*2*y-6.0621*15*z
        mech2left =-57.7350*x+-33.3333*2*y+6.0621*15*z

        scaled_mech1left = target_min + (mech1left-input_min)*(target_max-target_min)/(input_max-input_min)
        scaled_mech1right = target_min + (mech1right-input_min)*(target_max-target_min)/(input_max-input_min)
        scaled_mech2left = target_min + (mech2left-input_min)*(target_max-target_min)/(input_max-input_min)
        scaled_mech2right = target_min + (mech2right-input_min)*(target_max-target_min)/(input_max-input_min)

        mirte.setMotorSpeed('mech1left',int(scaled_mech1left))
        mirte.setMotorSpeed('mech1right',int(scaled_mech1right))
        mirte.setMotorSpeed('mech2left',int(scaled_mech2left))
        mirte.setMotorSpeed('mech2right',int(scaled_mech2right))

        print(int(scaled_mech1left), int(scaled_mech1right),int(scaled_mech2left),int(scaled_mech2right))



finally:
    conn.close()
    server_socket.close()
    ser.close()