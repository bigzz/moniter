#!/usr/bin/env python

__author__ = 'bigzhang'

try:
    import random
    import string
    import errno
    from os import getcwd
    from sys import stdin,exit
    from os.path import basename
    from os import mkdir
    from pyadb import ADB
except ImportError,e:
    print "[f] Required module missing. %s" % e.args[0]
    exit(-1)

def main():

    adb = ADB()

    # set ADB path
    adb.set_adb_path('/home/bigzhang/Android/Sdk/platform-tools/adb')

    print "[+] Using PyADB version %s" % adb.pyadb_version()

    # verity ADB path
    print "[+] Verifying ADB path...",
    if adb.check_path() is False:
        print "ERROR"
        exit(-2)
    print "OK"

    # print ADB Version
    print "[+] ADB Version: %s" % adb.get_version()

    print ""

    # restart server (may be other instances running)
    print "[+] Restarting ADB server..."
    adb.restart_server()
    if adb.lastFailed():
        print "\t- ERROR\n"
        exit(-3)

    # get detected devices
    dev = 0
    while dev is 0:
        print "[+] Detecting devices..." ,
        error,devices = adb.get_devices()

        if error is 1:
            # no devices connected
            print "No devices connected"
            print "[+] Waiting for devices..."
            adb.wait_for_device()
            continue
        elif error is 2:
            print "You haven't enought permissions!"
            exit(-3)

        print "OK"
        dev = 1

    # this should never be reached
    if len(devices) == 0:
        print "[+] No devices detected!"
        exit(-4)

    # show detected devices
    i = 0
    for dev in devices:
        print "\t%d: %s" % (i,dev)
        i += 1

    # if there are more than one devices, ask to the user to choose one of them
    if i > 1:
        dev = i + 1
        while dev < 0 or dev > int(i - 1):
            print "\n[+] Select target device [0-%d]: " % int(i - 1) ,
            dev = int(stdin.readline())
    else:
        dev = 0

    # set target device
    try:
        adb.set_target_device(devices[dev])
    except Exception,e:
        print "\n[!] Error:\t- ADB: %s\t - Python: %s" % (adb.get_error(),e.args)
        exit(-5)

    print "\n[+] Using \"%s\" as target device" % devices[dev]

    exit(0)

if __name__ == "__main__":
    main()