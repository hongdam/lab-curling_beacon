from curling import beacon
import socket
import sys
from datetime import datetime

HOST = ''
PORT = ''
BUFSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(ADDR)
except Exception as e:
    print("Can not connect to server")
    sys.exit()

print("connected")

while True:
    try:
        msg = client_socket.recv(BUFSIZE)
        some_state = True
        if some_state:
            file_title = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

            tr = beacon.start_collection()
            beacon.save_data(tr, file_title)
            beacon.draw_trajectory(tr)

    except KeyboardInterrupt:
        client_socket.close()
        break