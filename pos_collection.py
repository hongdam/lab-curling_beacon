from curling import beacon
import socket
import sys
from datetime import datetime

HOST = '192.168.0.250'
PORT = 8000
BUFSIZE = 1024
ADDR = (HOST, PORT)

# b'\xaa\x00\x02\x02\xaa\x00\x10\xaa\x00\x02\x02'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(ADDR)
except Exception as e:
    print("Can not connect to server")
    sys.exit()

print("connected")


def split_packet(packet):
    packet = packet.split(b'\xaa\x00')
    return [m for m in packet if len(m) != 0]


def wait_recv_return_title(title_flag=False):

    title_flag = title_flag
    start_flag = False
    title = ""
    while True:
        try:
            packet = client_socket.recv(BUFSIZE)
            packet = split_packet(packet)
            for p in packet:
                print(p)
                if p[0] == 25:
                    print("recv title")
                    title = p[1:-2]
                    title = title.decode('utf-8')
                    title_flag = True
                elif title_flag and p[0] == 4:
                    print("recv start")
                    start_flag = True

            if title_flag and start_flag:
                return True, title
        except KeyboardInterrupt:
            print("break wait_recv_return_title")
            return False, []

while True:
    try:
        #msg = client_socket.recv(BUFSIZE)

        # name 25 first, start 12 second
        # utf-8

        is_recv_t, title = wait_recv_return_title()

        if title == "":
            title = datetime.now().strftime('%m-%d_%H_%M_%S')

        if is_recv_t:
            #file_title = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            print("start collection")
            tr = beacon.start_collection()
            print("finish collection")
            beacon.save_data(tr, './data/'+title)
            beacon.draw_trajectory(tr, True, './data/'+title)
        else:
            client_socket.close()
            break

    except KeyboardInterrupt:
        client_socket.close()
        break