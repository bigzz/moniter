__author__ = 'bigzhang'

import csv_common

class gpuinfo:

    gpufile = 'gpuinfo.csv'

    gpufreq = []
    gpuload = []
    gpuinfo = [gpufreq, gpuload]

    write = 0
    read = 0

    def __init__(self, func_w, func_r):
        self.write = func_w
        self.read = func_r

    def update(self):


    def write(self):
        csv_common.csv_write(self.func_w, self.gpufile, self.gpuinfo)