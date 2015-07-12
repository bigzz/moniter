from pyadb.adb import ADB

__author__ = 'bigzhang'

import csv_common
from pyadb import ADB
import Queue
import string
import re
import time
import thread
#import matplotlib.pyplot as plt
import pylab as pl
from matplotlib import animation

online_cpu_path='/sys/devices/system/cpu/online'

freq_little_path='/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'
freq_big_path='/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq'

load_little_path='/sys/bus/cpu/devices/cpu0/cpufreq/interactive/cpu_util'
load_big_path='/sys/bus/cpu/devices/cpu4/cpufreq/interactive/cpu_util'

# CPU Info
class cpuinfo:
    cpufile = 'cpuinfo.csv'

    online = 0
    freq_l = [0]
    freq_b = [0]

    load_l = []
    load_l0 = [0] * 20
    load_l1 = [0] * 20
    load_l2 = [0] * 20
    load_l3 = [0] * 20

    load_b = []
    load_b4 = [0] * 20
    load_b5 = [0] * 20
    load_b6 = [0] * 20
    load_b7 = [0] * 20

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
            return 0

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
        if len(self.freq_l) >= 20:
            self.freq_l.pop(0)
        self.freq_l.append(self.get_freq_little())

        # Process Little CPU Load List
        self.load_l = self.get_load_little()
        if len(self.load_l0) >= 20:
            self.load_l0.pop(0)
            self.load_l1.pop(0)
            self.load_l2.pop(0)
            self.load_l3.pop(0)
        self.load_l0.append(self.load_l[0])
        self.load_l1.append(self.load_l[1])
        self.load_l2.append(self.load_l[2])
        self.load_l3.append(self.load_l[3])


        if(self.online > 3 ):
            # Process Big CPU Freq List
            if len(self.freq_b) >= 20:
                self.freq_b.pop(0)
            self.freq_b.append(self.get_freq_big())

            # Process B CPU Load List
            self.load_b = self.get_load_big()
            if len(self.load_b4) >= 20:
                self.load_b4.pop(0)
                self.load_b5.pop(0)
                self.load_b6.pop(0)
                self.load_b7.pop(0)
            self.load_b4.append(self.load_b[0])
            self.load_b5.append(self.load_b[1])
            self.load_b6.append(self.load_b[2])
            self.load_b7.append(self.load_b[3])
        else:
            self.freq_b.append(0)
            self.load_b = [0, 0, 0, 0]
            if len(self.load_b4) >= 20:
                self.load_b4.pop(0)
                self.load_b5.pop(0)
                self.load_b6.pop(0)
                self.load_b7.pop(0)
            self.load_b4.append(self.load_b[0])
            self.load_b5.append(self.load_b[1])
            self.load_b6.append(self.load_b[2])
            self.load_b7.append(self.load_b[3])

        #CPU All Info
        cinfo = [self.online, self.freq_l, self.load_l, self.freq_b, self.load_b]

        print cinfo

        #self.write(cinfo)

    def write(self, cpui):
        csv_common.csv_write(self.cpufile, cpui)

    def read(self, cpuinfo):
        cpucsv = open(self.cpufile, 'aw+')

cpuinfo_g = 0 #save cpuinfo

fig = pl.figure()
ax1 = fig.add_subplot(2,1,1,xlim=(0, 20), ylim=(0, 100))
ax2 = fig.add_subplot(2,1,2,xlim=(0, 20), ylim=(0, 100))
load_l0, = ax1.plot([], [], lw=2)
load_l1, = ax1.plot([], [], lw=2)
load_l2, = ax1.plot([], [], lw=2)
load_l3, = ax1.plot([], [], lw=2)

load_b4, = ax1.plot([], [], lw=2)
load_b5, = ax1.plot([], [], lw=2)
load_b6, = ax1.plot([], [], lw=2)
load_b7, = ax1.plot([], [], lw=2)

def init():
    load_l0.set_data([], [])
    load_l1.set_data([], [])
    load_l2.set_data([], [])
    load_l3.set_data([], [])
    return load_l0, load_l1, load_l2, load_l3

# animation function.  this is called sequentially
def animate(cpu):
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    cpuinfo_g = cpuinfo()
    load_l0.set_data(x, cpuinfo_g.load_l0)
    load_l1.set_data(x, cpuinfo_g.load_l1)
    load_l2.set_data(x, cpuinfo_g.load_l2)
    load_l3.set_data(x, cpuinfo_g.load_l3)

    load_b4.set_data(x, cpuinfo_g.load_b4)
    load_b5.set_data(x, cpuinfo_g.load_b5)
    load_b6.set_data(x, cpuinfo_g.load_b6)
    load_b7.set_data(x, cpuinfo_g.load_b7)
    return load_l0, load_l1, load_l2, load_l3, load_b4, load_b5, load_b6, load_b7

def load_show(cpu, interval=1):
    """
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    pl.plot(x, cpu.load_l0, 'r')
    pl.plot(x, cpu.load_l1, 'r')
    pl.plot(x, cpu.load_l2, 'r')
    pl.plot(x, cpu.load_l3, 'r')

    pl.plot(x, cpu.load_b4, 'g')
    pl.plot(x, cpu.load_b5, 'g')
    pl.plot(x, cpu.load_b6, 'g')
    pl.plot(x, cpu.load_b7, 'g')

    pl.title('CPU Load Info')
    pl.xlabel('Time')
    pl.ylabel('Load')
    pl.xlim(0.0, 20.0)
    pl.ylim(0.0, 100.0)
    """
    anim1 = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=0.1)
    pl.show()


def timer(cpu, times=0, interval=1):
    cnt = 0
    if times:
        while cnt < times:
            # print 'Thread:(%s) Time:%s/n'%(cnt, time.ctime())
            time.sleep(interval)
            cpu.update()
        thread.exit_thread()
    else:
        while True:
            time.sleep(interval)
            cpu.update()
        thread.exit_thread()

def update_thread(cpu):
    thread.start_new_thread(timer, (cpu, 100, 0.1))
    thread.start_new_thread(load_show, (cpu, 0.1))


def main():
    cpuin = cpuinfo()
    cpuinfo_g = cpuin
    update_thread(cpuin)
    while True:
        load_show(cpuin)
        time.sleep(1)

if __name__ == "__main__":
    main()
