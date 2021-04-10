from machine import Pin
from utime import sleep
import json
from ws2812b import ws2812b
import sys

with open("RGB.json", "r") as f:
    rgb = json.loads(f.read())
led = Pin(25, Pin.OUT)
neo = ws2812b(16,0,0)

activated = False

pinout = [2,3,4,18,6,7,8,9,10,11,12,13,14,15,17,16]
pins = []
remap = [0,1,2,3,7,6,5,4,8,9,10,11,15,14,13,12]
colors = [[50,50,50] for _ in range(16)]

# logo = [[1,0,0,0,
#          1,0,0,0,
#          1,0,0,0,
#          1,1,1,0],
#         [1,0,1,0,
#          1,0,1,0,
#          1,0,1,0,
#          1,1,1,0],
#         [1,0,0,0,
#          1,1,1,0,
#          1,0,1,0,
#          1,1,1,0], 
#         [1,1,1,0,
#          1,1,0,0,
#          1,0,0,0,
#          1,1,1,0]]

logo = [[1,1,1,0,
         1,0,0,0,
         1,0,0,0,
         1,0,0,0],
        [1,0,0,0,
         1,1,1,0,
         1,0,1,0,
         1,1,1,0],
        [1,1,1,1,
         1,0,0,1,
         1,0,0,1,
         1,1,1,1],
        [1,0,0,1,
         0,1,1,0,
         0,1,1,0,
         1,0,0,1]]

if(not activated):
    while True:
        led.toggle()
        sleep(1)


for c in logo:
    for lum in range(100):
        for bit in range(len(c)):
            if(c[bit] == 1):
                neo.set_pixel(remap[bit], 1 * (100-lum),1 * (100-lum),1 * (100-lum))
            else:
                neo.set_pixel(remap[bit], 0,0,0)
        neo.show()
        sleep(0.001)
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

while True:
    i = sys.stdin.read(6).split(".")
    neo.set_pixel(remap[int(i[0])], *rgb[int(i[1])])
    neo.show()
    with open("log.txt", "a") as file:
        file.write(i+"\n")