# from _marvelmind import MarvelmindHedge
from marvelmind import MarvelmindHedge
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

def start_collection():
    trajectory = []
    hedge = MarvelmindHedge(tty = "COM3", adr=10, debug=False, maxvaluescount=16, )
    hedge.start()
    while True:
        try:
            sleep(0.1)
            # print (hedge.position()) # get last position and print
            trajectory.append(hedge.position())
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            break
    return trajectory

def draw_trajectory(s_data):
    x = s_data[:, 1]
    y = s_data[:, 2]

    plt.scatter(y, x)
    plt.show()


def save_data(f_name, data):

    processed_data = []
    for x in data:
        if x[4] == 0:
            pass
        if len(processed_data) == 0:
            start_time = x[4]
        processed_time = x[4] - start_time

        if not processed_data:
            x = x[1:4] + [processed_time]
            processed_data.append(x)
        elif processed_data[-1][-1] != processed_time:
            x = x[1:4] + [processed_time]
            processed_data.append(x)

    with open(f_name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter='\n')
        writer.writerow(['\t'.join([str(j) for j in x]) for x in processed_data])

start_collection()