__author__ = 'bigzhang'

import csv

def csv_write(file, data):
    cpucsv = open(file, 'aw+')
    csvfile = csv.writer(cpucsv)
    csvfile.writerows(data)
    cpucsv.close()

def csv_read_cpuinfo(file, times):
    cpucsv = open(file, 'r')
    reader = csv.reader(cpucsv)

    cpucsv.close()
