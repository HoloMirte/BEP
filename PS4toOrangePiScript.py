import socket
import pygame

pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

def send_data(client_socket, data):
    try:
        client_socket.send(data.encode())
        print("Data sent")
    except Exception as e:
        print(f"Failed to send data: {e}")

client_socket = socket.socket()
host = '192.168.42.1'  # Replace with the actual IP address of your Orange Pi
port = 65432

try:
    print(f"Connecting to {host}:{port}")
    client_socket.connect((host, port))
    print("Connection established")

    while True:
        pygame.event.pump()
        x_axis = joystick.get_axis(0)  # X axis of the left joystick
        y_axis = joystick.get_axis(1)  # Y axis of the left joystick
        z_axis = joystick.get_axis(2)  # X axis of the right joystick
        data = f'X: {x_axis}, Y: {y_axis}, Z: {z_axis}'
        print(f"Sending data: {data}")
        send_data(client_socket, data)
        pygame.time.wait(100)

except Exception as e:
    print(f"Failed to connect or send data: {e}")
finally:
    client_socket.close()