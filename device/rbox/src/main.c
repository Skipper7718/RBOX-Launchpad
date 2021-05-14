#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include "pico/stdlib.h"
#include "pico/bootrom.h"
#include "hardware/gpio.h"
#include "../include/etc.h"
#include "../include/ws2812.h"

int main()
{
    stdio_init_all();
    init_ws2812();
    intro();

    for(;;)
    {
        char byte = getchar();
        printf("%c %d\n", byte, byte);
        if(byte == 97){
            attach_interrupts();
            fill_pixel(0,0,0);
            rboxcontrol();
        }
        else if(byte == 102){
            attach_interrupts();
            rboxtilt();
        }
    }
    
    return 0;
}