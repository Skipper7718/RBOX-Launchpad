from machine import Pin
from utime import sleep
from ws2812b import ws2812b
import sys

led = Pin(25, Pin.OUT)
neo = ws2812b(16,0,0)

pinout = [2,3,4,18,6,7,8,9,10,11,12,13,14,15,17,16]
pins = []
remap = [0,1,2,3,7,6,5,4,8,9,10,11,15,14,13,12]

lube = [[1,0,0,0,
         1,0,0,0,
         1,0,0,0,
         1,1,1,0],
        [1,0,1,0,
         1,0,1,0,
         1,0,1,0,
         1,1,1,0],
        [1,0,0,0,
         1,1,1,0,
         1,0,1,0,
         1,1,1,0],
        [1,1,1,0,
         1,1,0,0,
         1,0,0,0,
         1,1,1,0]]

for c in lube:
    for lum in range(100):
        for bit in range(len(c)):
            if(c[bit] == 1):
                neo.set_pixel(remap[bit], 1 * (100-lum),1*(100-lum),0)
            else:
                neo.set_pixel(remap[bit], 0,0,0)
        neo.show()
        sleep(0.01)
    for r in remap:
        neo.set_pixel(r, 0,0,0)
        neo.show()

neo.set_pixel(3,0,100,100)
neo.show()
byte = sys.stdin.read(1)
if(byte == "a"):
    for r in remap:
        neo.set_pixel(r, 0,0,0)
        neo.show()
else:
    machine.soft_reboot()

def toggle(pin):
    pin.irq(None)
    led.value(True)
    
    neo.set_pixel(remap[pins.index(pin)], 100,100,100)
    neo.show()
    
    sys.stdout.buffer.write(bytes([pins.index(pin)+1]))
    
    sleep(0.2)
    
    neo.set_pixel(remap[pins.index(pin)], 0,0,0)
    neo.show()
    
    led.value(False)
    
    pin.irq(toggle, Pin.IRQ_FALLING)

for pin in pinout:
    pins.append(Pin(pin, Pin.IN,Pin.PULL_UP))
for pin in pins:
    pin.irq(toggle, Pin.IRQ_FALLING)
