__author__ = 'bigzhang'

import csv

def csv_write(func, file, data):
    cpucsv = open(file, 'aw+')
    csvfile = csv.writer(cpucsv)
    csvfile.writerows(data)
    cpucsv.close()


def csv_read_cpuinfo(cpuinfo, time):
    cpucsv = open('cpuinfo.csv', 'r')
    reader = csv.reader(cpucsv)

    cpucsv.close()

def main():
    csv_write_cpuinfo(cpuinfo)

if __name__ == "__main__":
    main()