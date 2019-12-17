"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Sketch generator:           http://examples.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to initialize your ESP8266/ESP32 board
and connect it to Blynk.

Don't forget to change WIFI_SSID, WIFI_PASS and BLYNK_AUTH ;)
"""

import BlynkLib
import network
import machine
from Car import Car


WIFI_SSID = 'Maolin'
WIFI_PASS = 'WroomWroom'

#WIFI_SSID = 'AlsLUG'
#WIFI_PASS = 'TuxRocks'

BLYNK_AUTH = 'O_yxfSKYV0U2hVvHqhGHGFCi5nlifPXC'

print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    pass

myCar = Car()
myCar.setSpeed(50)
print('IP:', wifi.ifconfig()[0])

print("Connecting to Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH)



@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    

def runLoop():

    while True:
        blynk.run()
        machine.idle()

def limit( min, n, max):
    return sorted([min, n, max])[1]



# Register Virtual Pins
@blynk.VIRTUAL_WRITE(5)
def my_write_handler(value):
    myCar.coast()
    print('Coast: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(8)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.frem()
    else :
        myCar.coast()
    print('frem: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(2)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.bak()
    else :
        myCar.coast()
    print('bak: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(4)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.roterV()
    else :
        myCar.coast()
    print('roter venstre: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(6)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.roterH()
    else :
        myCar.coast()
    print('roterH: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(7)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.drejV()
    else :
        myCar.coast()
    print('drejV: {}'.format( value ) )

@blynk.VIRTUAL_WRITE(9)
def my_write_handler(value):
    if value[0] == '1' :
        myCar.drejH()
    else :
        myCar.coast()
    print('drejH: {}'.format( value ) )

# Run blynk in the main thread:
runLoop()

# Or, run blynk in a separate thread (unavailable for esp8266):
#import _thread
#_thread.stack_size(5*1024)
#_thread.start_new_thread(runLoop, ())


# Note:
# Threads are currently unavailable on some devices like esp8266
# ESP32_psRAM_LoBo has a bit different thread API:
# _thread.start_new_thread("Blynk", runLoop, ())
