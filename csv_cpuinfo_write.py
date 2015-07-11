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

online_cpu_path='/sys/devices/system/cpu/online'

freq_little_path='/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'
freq_big_path='/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq'

load_little_path='/sys/bus/cpu/devices/cpu0/cpufreq/interactive/cpu_util'
load_big_path='/sys/bus/cpu/devices/cpu4/cpufreq/interactive/cpu_util'

# CPU Info
class cpuinfo:
    cpufile = 'cpuinfo.csv'

    online = 0
    freq_l = 0
    freq_b = 0
    load_l = 0
    load_b = 0
    cpuinfo = Queue.Queue(maxsize = 10)

    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')

    def __init__(self, size):
        if(size != 10):
            self.cpuinfo = Queue.Queue(size)

    def get_online_cpu(self):
        online_cpu_cmd = 'cat ' + online_cpu_path
        tmp = self.adb.shell_command(online_cpu_cmd)
        #online = re.findall(r"\d+\.?\d+", tmp)
        online = tmp[2]
        return online

    def get_freq_little(self):
        freq_little_cmd = 'cat ' + freq_little_path
        tmp = self.adb.shell_command(freq_little_cmd)
        #print tmp
        freq_l = re.findall(r"\d+\.?\d+", tmp)
        return freq_l

    def get_load_little(self):
        load_little_cmd = 'cat ' + load_little_path
        tmp = self.adb.shell_command(load_little_cmd)
        #print tmp
        load_l = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_l) < 4):
            load_l.append('0')

        return load_l

    def get_freq_big(self):
        freq_big_cmd = 'cat ' + freq_big_path
        tmp = self.adb.shell_command(freq_big_cmd)
        #print tmp
        freq_b = re.findall(r"\d+\.?\d+", tmp)
        if freq_b:
            return freq_b
        else:
            return '0'

    def get_load_big(self):
        load_big_cmd = 'cat ' + load_big_path
        tmp = self.adb.shell_command(load_big_cmd)
        #print tmp
        load_b = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_b) < 4):
            load_b.append('0')

        return load_b

    def update(self):
        self.online = self.get_online_cpu()
        self.freq_l = self.get_freq_little()
        self.load_l = self.get_load_little()
        if(string.atoi(self.online) > 3 ):
            self.freq_b = self.get_freq_big()
            self.load_b = self.get_load_big()
        else:
            self.freq_b = '0'
            self.load_b = ['0', '0', '0', '0']

        info = [self.online, self.freq_l, self.load_l, self.freq_b, self.load_b]

        if self.cpuinfo.full():
            print self.cpuinfo.get()

        self.cpuinfo.put(info)

        #print info
        #print self.cpuinfo.qsize()

        self.write(info)

    def write(self, cpui):
        csv_common.csv_write(self.cpufile, cpui)

    def read(self, cpuinfo):
        cpucsv = open(self.cpufile, 'aw+')


def timer(cpu, times = 0 , interval = 1):
    cnt = 0
    if times:
        while cnt < times:
            # print 'Thread:(%s) Time:%s/n'%(cnt, time.ctime())
            time.sleep(interval)
            cpu.update()
        thread.exit_thread()
    else:
        while True:
            cpu.update()
        thread.exit_thread()

def update_thread(cpu):
    thread.start_new_thread(timer, (cpu, 100, 1))



def mulitplot_pic():
    x1 = [1, 2, 3, 4, 5]
    y1 = [1, 4, 9, 16, 25]
    x2 = [1, 2, 4, 6, 8]
    y2 = [2, 4, 8, 12, 16]
    pl.plot(x1, y1, 'r')
    pl.plot(x2, y2, 'g')
    pl.title('Plot of y vs. x')
    pl.xlabel('x axis')
    pl.ylabel('y axis')
    pl.xlim(0.0, 9.0)
    pl.ylim(0.0, 30.)
    pl.show()

def main():
    cpuin = cpuinfo(20)
    update_thread(cpuin)
    mulitplot_pic()
    time.sleep(10000)


if __name__ == "__main__":
    main()
