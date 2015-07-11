__author__ = 'bigzhang'

import csv_common
from pyadb import ADB
import Queue
import string
import re

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

    def __init__(self, func_w, func_r, size):
        self.write = func_w
        self.read = func_r
        if(size != 10):
            self.cpuinfo = Queue.Queue(size)

    def get_online_cpu(self):
        online_cpu_cmd = 'cat ' + online_cpu_path
        tmp = self.adb.shell_command(online_cpu_cmd)
        #online = re.findall(r"\d+\.?\d+", tmp)
        online = tmp[2]
        return online
        #print self.adb.shell_command(online_cpu_cmd)

    def get_freq_little(self):
        freq_little_cmd = 'cat ' + freq_little_path
        tmp = self.adb.shell_command(freq_little_cmd)
        freq_l = re.findall(r"\d+\.?\d+", tmp)
        return freq_l
        #print self.adb.shell_command(freq_little_cmd)

    def get_load_little(self):
        load_little_cmd = 'cat ' + load_little_path
        tmp = self.adb.shell_command(load_little_cmd)
        load_l = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_l) < 4):
            load_l.append('0')

        return load_l
        #print self.adb.shell_command(load_little_cmd)

    def get_freq_big(self):
        freq_big_cmd = 'cat ' + freq_big_path
        return self.adb.shell_command(freq_big_cmd)
        freq_b = re.findall(r"\d+\.?\d+", tmp)
        return freq_b
        #print self.adb.shell_command(freq_big_cmd)

    def get_load_big(self):
        load_big_cmd = 'cat ' + load_big_path
        tmp = self.adb.shell_command(load_big_cmd)
        load_b = re.findall(r"\d+\.?\d+", tmp)

        while(len(load_b) < 4):
            load_b.append('0')

        return load_b
        #print self.adb.shell_command(load_big_cmd)

    def update(self):
        self.online = self.get_online_cpu()
        self.freq_l = self.get_freq_little()
        self.load_l = self.get_load_little()
        if(string.atoi(self.online) > 3 ):
            self.freq_b = self.get_freq_big()
            self.load_b = self.get_load_big()
        else:
            self.freq_b = 0
            self.load_b = ['0', '0', '0', '0']

        info = [self.online, self.freq_l, self.load_l, self.freq_b, self.load_b]

        self.cpuinfo.put(info)

        print self.cpuinfo.get()
        print self.cpuinfo.get()

    def write(self, func, cpuinfo):
        csv_common.csv_write(self.func, self.cpufile, self.cpuinfo)

    def read(self, cpuinfo):
        cpucsv = open(self.cpufile, 'aw+')


def main():
    cpui = cpuinfo(0, 0, 20)
    cpui.update()


if __name__ == "__main__":
    main()
