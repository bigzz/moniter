__author__ = 'bigzhang'

from pyadb import ADB
import re
import threading
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from scipy.interpolate import spline

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
        if len(self.gpu_load) >= self.maxnum:
            self.gpu_load.pop(0)
        self.gpu_load.append(self.get_load_gpu()[0])

        if len(self.gpu_freq) >= self.maxnum:
            self.gpu_freq.pop(0)
        self.gpu_freq.append(self.get_freq_gpu()[0])

        print self.gpu_load
        print self.gpu_freq

gpuinfo_g = 0

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1, xlim=(0, 50), ylim=(0, 100))
ax2 = fig.add_subplot(2, 1, 2, xlim=(0, 50), ylim=(0, 1000))

load, = ax1.plot([], [], lw=1)
freq, = ax2.plot([], [], lw=1)


def init():
    load.set_data([], [])
    freq.set_data([], [])

    return load, freq

def animate(gpu):
    x = range(50)
    gpuinfo_g = gpuinfo()

    gpulock.acquire()
    y_load = gpuinfo_g.gpu_load
    y_freq = gpuinfo_g.gpu_freq

    x_sm = np.array(x)
    y_sm_l = np.array(y_load)
    y_sm_f = np.array(y_freq)

    x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
    y_smooth_l = spline(x, y_sm_l, x_smooth)
    y_smooth_f = spline(x, y_sm_f, x_smooth)

    load.set_data(x_smooth, y_smooth_l)
    freq.set_data(x_smooth, y_smooth_f)
    gpulock.release()

    return load, freq

def load_show():
    am = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=1)
    plt.show()


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

    load_show()
    update.join()

    time.sleep(10000)

if __name__ == "__main__":
    main()