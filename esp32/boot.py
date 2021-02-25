# This file is executed on every boot (including wake-boot from deepsleep)
import uos, machine
import gc
import webrepl
gc.collect()
#machine.freq(160000000)

#import network
#ap = network.WLAN(network.AP_IF)
#ap.active(True)
#ap.config(essid='zlaps_sensor')
#ap.config(authmode=3, password='zlaps_sensor_123')

#while ap.active() == False:
#  print('Waiting for connection...')

#print('Connection successful')
#print(ap.ifconfig())

#webrepl.start()
