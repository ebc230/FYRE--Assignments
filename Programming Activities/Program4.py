# This program was created in Arduino Lab for MicroPython
from machine import Pin
import time

led = Pin(0, machine.Pin.OUT) #saving led pin info in variable, 0 pin num and set mode to output
led.value(1) #1, turns led light on (0 for off)

while True: #repeats infinetly, always True
  led.value(1) #turns LED on
  time.sleep(1) # 1 second wait
  led.value(0) # turns LED off
  time.sleep(1) # 1 second wait
  
