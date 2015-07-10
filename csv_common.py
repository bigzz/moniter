__author__ = 'bigzhang'

import csv


online = [6]
cpufreq = [800000, 1200000]
cpuload_l = [100, 100, 100, 0]
cpuload_b = [100, 100, 100, 0]

cpuinfo = [online, cpufreq, cpuload_l, cpuload_b]


def csv_write_cpuinfo(cpuinfo):
    cpucsv = open('cpuinfo.csv', 'aw+')
    csvfile = csv.writer(cpucsv)
    csvfile.writerows(cpuinfo)
    cpucsv.close()


def csv_read_cpuinfo(cpuinfo, time):
    cpucsv = open('cpuinfo.csv', 'r')
    reader = csv.reader(cpucsv)

    cpucsv.close()

def main():
    csv_write_cpuinfo(cpuinfo)

if __name__ == "__main__":
    main()