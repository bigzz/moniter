__author__ = 'bigzhang'

import csv

def csv_write_cpu(cpuinfo):
    cpucsv = open('cpuinfo.csv', 'w')
    csvfile = csv.writer(cpucsv)
    csvfile.writerows(cpuinfo)    "write cpuinfo to csv file"
    cpucsv.close()


def csv_write_cpu(cpuinfo, time):
    cpucsv = open('cpuinfo.csv', 'r')
    reader = csv.reader(cpucsv)

    cpucsv.close()