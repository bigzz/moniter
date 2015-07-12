__author__ = 'bigzhang'

from pyadb import ADB

"""
# GPU
power_gpu_path=/sys/bus/platform/devices/14ac0000.mali/power_state
freq_gpu_path=/sys/bus/platform/devices/14ac0000.mali/clock
load_gpu_path=/sys/bus/platform/devices/14ac0000.mali/utilization
"""

power_gpu_path='/sys/bus/platform/devices/14ac0000.mali/power_state'
freq_gpu_path='/sys/bus/platform/devices/14ac0000.mali/clock'
load_gpu_path='/sys/bus/platform/devices/14ac0000.mali/utilization'

def get_freq_gpu(adb):
    freq_gpu_cmd = 'cat ' + freq_gpu_path
    print adb.shell_command(freq_gpu_cmd)

def get_load_gpu(adb):
    load_gpu_cmd = 'cat ' + load_gpu_path
    print adb.shell_command(load_gpu_cmd)

def main():

    adb = ADB()
    # set ADB path
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')

    get_freq_gpu(adb)
    get_load_gpu(adb)

if __name__ == "__main__":
    main()