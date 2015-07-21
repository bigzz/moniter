__author__ = 'bigzhang'

from pyadb import ADB
import re
import threading
import time

power_gpu_path='/sys/bus/platform/devices/14ac0000.mali/power_state'
freq_gpu_path='/sys/bus/platform/devices/14ac0000.mali/clock'
load_gpu_path='/sys/bus/platform/devices/14ac0000.mali/utilization'

class gpuinfo:
    cpufile = 'gpuinfo.csv'
    maxnum = 50

    gpu_load = [0] * maxnum
    gpu_freq = [0] * maxnum

    adb = ADB()
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')
    adb.get_devices()
    adb.set_target_device('123456789ABC')

    def get_freq_gpu(self):
        freq_gpu_cmd = 'cat ' + freq_gpu_path
        tmp = self.adb.shell_command(freq_gpu_cmd)
        print tmp

        freq = re.findall(r"\d+\.?\d+", tmp)
        return map(int, freq)

    def get_load_gpu(self):
        load_gpu_cmd = 'cat ' + load_gpu_path
        tmp = self.adb.shell_command(load_gpu_cmd)
        print tmp

        load = re.findall(r"\d+\.?\d+", tmp)
        return map(int, load)

    def update(self):
        self.get_freq_gpu()
        self.get_load_gpu()

gpulock = threading.RLock()

class update_thread(threading.Thread):
    def __init__(self, gpu, interval):
        threading.Thread.__init__(self)
        self.gpuinf = gpu
        self.interval = interval
    def run(self):
        while True:
            time.sleep(self.interval)
            gpulock.acquire()
            self.gpuinf.update()
            gpulock.release()

def main():
    gpuin = gpuinfo()
    update = update_thread(gpuin, 1)
    update.start()

    time.sleep(10000)

if __name__ == "__main__":
    main()