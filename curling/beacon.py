from .marvelmind import MarvelmindHedge
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import csv


def start_collection(tty="COM3"):
    trajectory = []
    hedge = MarvelmindHedge(tty=tty, adr=10, debug=False, maxvaluescount=16)
    hedge.start()
    while True:
        start_time = 0
        try:
            sleep(0.1)
            # print (hedge.position()) # get last position and print
            p = hedge.position()
            if p[4] != 0:
                start_time = p[4]
            else:
                pass
            p[4] -= start_time

            # de-duplication
            if trajectory[-1][-1] == p[4]:
                pass

            # find finish time and stop
            if len(trajectory) > 30 and dist(trajectory) < 0.05:
                hedge.stop()
                break

            trajectory.append(p[1:])

        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            break
    return trajectory


def dist(a, b):
    return np.sqrt(np.sum(np.power(a-b, 2)))


def draw_trajectory(s_data):
    s_data = np.array(s_data)
    x = s_data[:, 1]
    y = s_data[:, 2]

    plt.axis('equal')
    plt.scatter(y, x)
    plt.show()


def save_data(f_name, data):

    with open(f_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(['\t'.join([str(j) for j in i]) for i in data])
