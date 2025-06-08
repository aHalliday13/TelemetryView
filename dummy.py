"""
Simulates a TeleBT sending basic telemetry over a serial port. 
For testing purposes only.
"""

from pyvirtualserial import VirtualSerial
from time import sleep
from random import randbytes
from time import time_ns

dongle = VirtualSerial()
print(dongle.get_slave_name())

height = 0
speed = 0

tick_start = time_ns() // 10000000

while True:
    tick = (time_ns() // 10000000) - tick_start
    print(tick)
    tick_h = tick.to_bytes(2).hex()

    speed_h = speed.to_bytes(2).hex()
    height_h = height.to_bytes(2).hex()
    
    telem = f"TELEM 22beef{tick_h}0a0000000000000000000000{speed_h}{height_h}aaaabbbbcccc000000000000ffffff\n"

    print(telem)

    telem = telem.encode()

    dongle.write(telem)
    sleep(0.01)

    speed += 1
    height += 1

    telem = ""
