from .marvelmind import MarvelmindHedge
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime


def start_collection():
    trajectory = []
    hedge = MarvelmindHedge(tty="COM3", adr=10, debug=False, maxvaluescount=16)
    hedge.start()
    while True:
        try:
            sleep(0.1)
            # print (hedge.position()) # get last position and print

            p = hedge.position()[1:]
            if p[1] > -9.5:
                trajectory.append(p)

            if len(trajectory) > 40 and dist(trajectory[-10][1:3], trajectory[-1][1:3]) < 0.05:
                hedge.stop()
                break

        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            break
    return data_processing(trajectory)


def data_processing(data):

    start_time = 0
    trajectory = []

    for p in data:
        p_c = p[:]

        # check garbage
        if p_c[3] == 0:
            continue

        p_c[3] -= start_time

        # de-duplication
        if len(trajectory) == 0:
            start_time = p_c[3]
            p_c[3] = 0
        elif trajectory[-1][-1] == p_c[3]:
            continue
        trajectory.append(p_c)

    return trajectory


def dist(a, b):

    a = np.array(a)
    b = np.array(b)

    dist_a_b = np.sqrt(np.sum(np.power(a - b, 2)))
    # print(dist_a_b)
    return dist_a_b


def draw_trajectory(s_data):

    s_data = np.array(s_data)
    x = s_data[:, 1]
    y = s_data[:, 2]

    plt.axis('equal')
    plt.scatter(y, x, s=2)
    plt.show()


def save_data(data, f_name=None):
    if f_name is None:
        f_name = './data/' + datetime.now().strftime('%m-%d_%H_%M_%S')

    with open(f_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(['\t'.join([str(j) for j in i]) for i in data])
