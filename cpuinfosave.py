__author__ = 'bigzhang'

from pyadb import ADB

"""
online_cpu_path=/sys/devices/system/cpu/online

freq_little_path=/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
freq_big_path=/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq

load_little_path=/sys/bus/cpu/devices/cpu0/cpufreq/interactive/cpu_util
load_big_path=/sys/bus/cpu/devices/cpu4/cpufreq/interactive/cpu_util
"""

online_cpu_path='/sys/devices/system/cpu/online'

freq_little_path='/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq'
freq_big_path='/sys/devices/system/cpu/cpu4/cpufreq/scaling_cur_freq'

load_little_path='/sys/bus/cpu/devices/cpu0/cpufreq/interactive/cpu_util'
load_big_path='/sys/bus/cpu/devices/cpu4/cpufreq/interactive/cpu_util'


def get_online_cpu(adb):
    online_cpu_cmd = 'cat ' + online_cpu_path
    print adb.shell_command(online_cpu_cmd)

def get_frqe_little(adb):
    freq_little_cmd = 'cat ' + freq_little_path
    print adb.shell_command(freq_little_cmd)

def get_load_little(adb):
    freq_little_cmd = 'cat ' + load_little_path
    print adb.shell_command(freq_little_cmd)

def get_freq_big(adb):
    freq_big_cmd = 'cat ' + freq_big_path
    print adb.shell_command(freq_big_cmd)

def get_load_big(adb):
    load_big_cmd = 'cat ' + load_big_path
    print adb.shell_command(load_big_cmd)

def main():

    adb = ADB()
    # set ADB path
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')
    get_online_cpu(adb)

    get_frqe_little(adb)
    get_load_little(adb)

    get_freq_big(adb)
    get_load_big(adb)

if __name__ == "__main__":
    main()