import json, sys
from machine import Pin
from utime import sleep
from ws2812b import ws2812b

### SETUP ###

#load rgb
with open("RGB.json", "r") as f:
    rgb = json.loads(f.read())

#create onboard led and neopixel device
led = Pin(25, Pin.OUT)
neo = ws2812b(16,0,0)

#change debug to false if device should not interact with anything
#used only for debugging and maintenance
activated = True

pins = [] #button objects will be stored here

#buttons the pins are connected to
pinout = [2,3,4,18,6,7,8,9,10,11,12,13,14,15,17,16]

#neopixel stripe is not mathcing the button in terms of index, so rows 2 and 4 sre inverted
remap = [0,1,2,3,7,6,5,4,8,9,10,11,15,14,13,12]

#define text for startup
logo = [[1,1,1,0,
         1,0,1,0,
         1,1,0,0,
         1,0,1,0],
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

#if device is not activated, blink eternally
if(not activated):
    while True:
        led.toggle()
        sleep(1)

#smal pulse animation :)
for c in logo:
    for lum in range(100):
        for bit in range(len(c)):
            if(c[bit] == 1):
                neo.set_pixel(remap[bit], 1 * (100-lum),1 * (100-lum),1 * (100-lum))
            else:
                neo.set_pixel(remap[bit], 0,0,0)
        neo.show()
        sleep(0.001)

    #blank leds after ineration
    for r in remap:
        neo.set_pixel(r, 0,0,0)
        neo.show()

#show that device is ready to be connected to driver
neo.set_pixel(3,0,100,100)
neo.show()

#functions that is called when device is in performance mode
def main_rbox():

    #pin toggle interrupt
    def toggle(pin):
        pin.irq(None) #turn interrupt off for button debouncing

        led.value(True) #blink led to show that a button is pressed
        
        sys.stdout.buffer.write(bytes([pins.index(pin)]))
        
        sleep(0.2) #sleep for debounce
        
        led.value(False)
        
        pin.irq(toggle, Pin.IRQ_FALLING) #turn interrupt on again

    #create pins objects and turn on interrupts
    for pin in pinout:
        pins.append(Pin(pin, Pin.IN,Pin.PULL_UP))
    for pin in pins:
        pin.irq(toggle, Pin.IRQ_FALLING)

    #loop for handling rgb signals
    while True:
        i = sys.stdin.read(6).split(".")
        neo.set_pixel(remap[int(i[0])], *rgb[int(i[1])])
        neo.show()

#check mode that the launchpad shoudl start in
#only one for now, a color config tools will be added soon

byte = sys.stdin.read(1) #read a single byte

if(byte == "a"):
    neo.fill(0,0,0)
    neo.show()
    main_rbox() #call performance mode
else:
    machine.soft_reboot() #reboot
