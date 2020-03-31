#!/usr/bin/env python

# Default boot script

from machine import UART, RTC
import machine
import os
from network import WLAN

print("Booting")

#
# Init wifi
#
print("Initializing WiFi")
SSID = ''
KEY = ''

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, KEY), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        print(wlan.ifconfig()) # Print the connection settings, IP, Subnet mask, Gateway, DNS
        break


#
# Setup the time of the device
#
print("Initializing NTP time server")
rtc = RTC()
rtc.ntp_sync("pool.ntp.org") # Sync with time server

uart = UART(0, baudrate=115200)
os.dupterm(uart)

print("Start executing main.py")
machine.main('main.py')