from pyadb.adb import ADB

__author__ = 'bigzhang'

import csv_common
from pyadb import ADB
import string
import re
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.interpolate import spline

online_cpu_path='/sys/devices/system/cpu/online'

freq_little_path='/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'
freq_big_path='/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq'

load_little_path='/sys/bus/cpu/devices/cpu0/cpufreq/interactive/cpu_util'
load_big_path='/sys/bus/cpu/devices/cpu4/cpufreq/interactive/cpu_util'

# CPU Info
class cpuinfo:
    cpufile = 'cpuinfo.csv'
    maxnum = 50
    online = 0
    freq_l = [0] * maxnum
    freq_b = [0] * maxnum

    load_l = []
    load_b = []
    load_sum_l = [0] * maxnum
    load_sum_b = [0] * maxnum

    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')

    def __init__(self):
        self.online = 0

    def get_online_cpu(self):
        online_cpu_cmd = 'cat ' + online_cpu_path
        tmp = self.adb.shell_command(online_cpu_cmd)
        #online = re.findall(r"\d+\.?\d+", tmp)
        online = tmp[2]
        return string.atoi(online)

    def get_freq_little(self):
        freq_little_cmd = 'cat ' + freq_little_path
        tmp = self.adb.shell_command(freq_little_cmd)
        #print tmp
        freq_l = re.findall(r"\d+\.?\d+", tmp)
        return map(int, freq_l)

    def get_load_little(self):
        load_little_cmd = 'cat ' + load_little_path
        tmp = self.adb.shell_command(load_little_cmd)
        #print tmp
        load_l = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_l) < 4):
            load_l.append('0')

        return map(int, load_l)

    def get_freq_big(self):
        freq_big_cmd = 'cat ' + freq_big_path
        tmp = self.adb.shell_command(freq_big_cmd)
        #print tmp
        freq_b = re.findall(r"\d+\.?\d+", tmp)
        if freq_b:
            return map(int, freq_b)
        else:
            return [0]

    def get_load_big(self):
        load_big_cmd = 'cat ' + load_big_path
        tmp = self.adb.shell_command(load_big_cmd)
        #print tmp
        load_b = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_b) < 4):
            load_b.append('0')

        return map(int, load_b)

    def update(self):
        self.online = self.get_online_cpu()

        # Process Little CPU Freq List
        if len(self.freq_l) >= self.maxnum:
            self.freq_l.pop(0)
        self.freq_l.append(self.get_freq_little()[0])

        # Process Little CPU Load List
        self.load_l = self.get_load_little()
        if len(self.load_sum_l) >= self.maxnum:
            self.load_sum_l.pop(0)
        self.load_sum_l.append(self.load_l[0] + self.load_l[1] + self.load_l[2] + self.load_l[3])

        if(self.online > 3 ):
            # Process Big CPU Freq List
            if len(self.freq_b) >= self.maxnum:
                self.freq_b.pop(0)
            self.freq_b.append(self.get_freq_big()[0])

            # Process B CPU Load List
            self.load_b = self.get_load_big()
            if len(self.load_sum_b) >= self.maxnum:
                self.load_sum_b.pop(0)
            self.load_sum_b.append(self.load_b[0] + self.load_b[1] + self.load_b[2] + self.load_b[3])
        else:
            if len(self.freq_b) >= self.maxnum:
                self.freq_b.pop(0)
            self.freq_b.append(0)

            self.load_b = [0, 0, 0, 0]
            if len(self.load_sum_b) >= self.maxnum:
                self.load_sum_b.pop(0)
            self.load_sum_b.append(0)

        #CPU All Info
        cinfo = [self.online, self.freq_l, self.load_l, self.freq_b, self.load_b]

        #print cinfo

        #self.write(cinfo)

    def write(self, cpui):
        csv_common.csv_write(self.cpufile, cpui)

    def read(self, cpuinfo):
        cpucsv = open(self.cpufile, 'aw+')

cpuinfo_g = 0 #save cpuinfo

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1, xlim=(0, 50), ylim=(0, 400))
ax2 = fig.add_subplot(2, 1, 2, xlim=(0, 50), ylim=(0, 2500000))

load_sum_l, = ax1.plot([], [], lw=2)
load_sum_b, = ax1.plot([], [], lw=2)
freq_l, = ax2.plot([], [], lw=2)
freq_b, = ax2.plot([], [], lw=2)

def init():
    load_sum_l.set_data([], [])
    load_sum_b.set_data([], [])
    freq_l.set_data([], [])
    freq_b.set_data([], [])

    return load_sum_l, load_sum_b, freq_l, freq_b

def animate(cpu):
    x = range(50)
    cpuinfo_g = cpuinfo()

    y = cpuinfo_g.load_sum_l
    x_sm = np.array(x)
    y_sm = np.array(y)

    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth = spline(x, y, x_smooth)

    cpulock.acquire()
    load_sum_l.set_data(x_smooth, y_smooth)
    load_sum_b.set_data(x, cpuinfo_g.load_sum_b)

    freq_l.set_data(x, cpuinfo_g.freq_l)
    freq_b.set_data(x, cpuinfo_g.freq_b)
    cpulock.release()

    return load_sum_l, load_sum_b, freq_l, freq_b

def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=1/100)
    plt.show()

cpulock = threading.RLock()

class update_thread(threading.Thread):
    def __init__(self, cpu, interval):
        threading.Thread.__init__(self)
        self.cpuinf = cpu
        self.interval = interval
    def run(self):
        while True:
            time.sleep(self.interval)
            cpulock.acquire()
            self.cpuinf.update()
            cpulock.release()

def main():
    cpuin = cpuinfo()
    update = update_thread(cpuin, 1)
    update.start()

    load_show()
    update.join()

    time.sleep(10000)

if __name__ == "__main__":
    main()
