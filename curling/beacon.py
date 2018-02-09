from .marvelmind import MarvelmindHedge
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime


def start_collection(save=False):
    trajectory = []
    hedge = MarvelmindHedge(tty="COM3", adr=10, debug=False, maxvaluescount=16)
    hedge.start()
    while True:
        try:
            sleep(0.1)
            # print (hedge.position()) # get last position and print

            p = hedge.position()[1:]
            #print(p[0])
            if p[1] > -4.3:
                trajectory.append(p)

            if len(trajectory) > 40 and dist(trajectory[-15][1:3], trajectory[-1][1:3]) < 0.05:
                hedge.stop()
                break

        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            break

    trajectory = data_processing(trajectory)
    if save:
        save_data(trajectory)

    return trajectory


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


def draw_trajectory(s_data, save=False, f_name=None):

    s_data = np.array(s_data)
    x = s_data[:, 0]
    y = s_data[:, 1]

    plt.axis('equal')
    plt.scatter(x, y, s=2)
    if save:
        if f_name == None:
            f_name = datetime.now().strftime('%m-%d_%H_%M_%S')
        plt.savefig(f_name)
        plt.clf()
    else:
        plt.show()


def save_data(data, f_name=None):
    if f_name is None:
        f_name = './data/' + datetime.now().strftime('%m-%d_%H_%M_%S')

    with open(f_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(['\t'.join([str(j) for j in i]) for i in data])


def load_data(f_name):

    with open(f_name, 'r') as file:
        data = [[float(d) for d in line.split()] for line in file if len(line) > 1]

    return data
