#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "pico/stdlib.h"
#include "pico/bootrom.h"
#include "hardware/gpio.h"
#include "../include/etc.h"
#include "../include/ws2812.h"

static const uint8_t sins[360] = {
  127,129,131,134,136,138,140,143,145,147,149,151,154,156,158,160,162,164,166,169,171,173,175,177,179,181,183,185,187,189,191,193,195,196,198,200,
  202,204,205,207,209,211,212,214,216,217,219,220,222,223,225,226,227,229,230,231,233,234,235,236,237,239,240,241,242,243,243,244,245,246,247,248,
  248,249,250,250,251,251,252,252,253,253,253,254,254,254,254,254,254,254,255,254,254,254,254,254,254,254,253,253,253,252,252,251,251,250,250,249,
  248,248,247,246,245,244,243,243,242,241,240,239,237,236,235,234,233,231,230,229,227,226,225,223,222,220,219,217,216,214,212,211,209,207,205,204,
  202,200,198,196,195,193,191,189,187,185,183,181,179,177,175,173,171,169,166,164,162,160,158,156,154,151,149,147,145,143,140,138,136,134,131,129,
  127,125,123,120,118,116,114,111,109,107,105,103,100,98,96,94,92,90,88,85,83,81,79,77,75,73,71,69,67,65,63,61,59,58,56,54,
  52,50,49,47,45,43,42,40,38,37,35,34,32,31,29,28,27,25,24,23,21,20,19,18,17,15,14,13,12,11,11,10,9,8,7,6,
  6,5,4,4,3,3,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,2,2,3,3,4,4,5,
  6,6,7,8,9,10,11,11,12,13,14,15,17,18,19,20,21,23,24,25,27,28,29,31,32,34,35,37,38,40,42,43,45,47,49,50,
  52,54,56,58,59,61,63,65,67,69,71,73,75,77,79,81,83,85,88,90,92,94,96,98,100,103,105,107,109,111,114,116,118,120,123,125
};

static const int RGB[128][3] = {
    {43,89,90},
    {28,28,28},
    {124,124,124},
    {152,152,152},
    {255,77,71},
    {255,10,0},
    {90,1,0},
    {25,0,0},
    {255,189,98},
    {255,86,0},
    {90,29,0},
    {36,24,0},
    {253,253,33},
    {253,253,0},
    {88,88,0},
    {24,24,0},
    {128,253,42},
    {64,253,0},
    {22,88,0},
    {19,40,0},
    {52,253,43},
    {0,253,0},
    {0,88,0},
    {0,24,0},
    {51,253,70},
    {0,253,0},
    {0,88,0},
    {0,24,0},
    {50,253,126},
    {0,253,58},
    {0,0,255},
    {255,255,255},
    {47,252,176},
    {0,252,145},
    {0,88,49},
    {0,24,15},
    {57,191,255},
    {0,167,255},
    {0,64,81},
    {0,16,24},
    {65,134,255},
    {0,80,255},
    {0,26,90},
    {0,7,25},
    {0,0,0},
    {0,0,0},
    {0,0,91},
    {0,0,255},
    {131,71,255},
    {80,0,255},
    {22,0,103},
    {11,0,50},
    {255,73,255},
    {255,0,255},
    {90,0,90},
    {25,0,25},
    {255,77,132},
    {255,7,82},
    {90,1,27},
    {33,0,16},
    {255,25,0},
    {155,53,0},
    {17,0,80},
    {255,255,10},
    {0,56,0},
    {0,84,50},
    {0,83,126},
    {0,0,255},
    {0,68,77},
    {27,0,210},
    {124,124,124},
    {32,32,32},
    {255,10,0},
    {186,253,0},
    {170,237,0},
    {86,253,0},
    {0,136,0},
    {0,252,122},
    {0,167,255},
    {0,27,255},
    {53,0,255},
    {119,0,255},
    {180,23,126},
    {65,32,0},
    {255,74,0},
    {131,225,0},
    {101,253,0},
    {0,253,0},
    {0,253,0},
    {69,253,97},
    {0,252,202},
    {80,134,255},
    {39,77,201},
    {130,122,237},
    {211,12,255},
    {255,6,90},
    {255,125,0},
    {185,177,0},
    {138,253,0},
    {130,93,0},
    {57,40,0},
    {13,76,5},
    {0,80,55},
    {19,19,41},
    {16,31,90},
    {106,60,23},
    {172,4,0},
    {225,81,53},
    {220,105,0},
    {255,225,0},
    {153,225,0},
    {95,181,0},
    {27,27,49},
    {220,253,84},
    {118,252,184},
    {150,151,255},
    {139,97,255},
    {64,64,64},
    {116,116,116},
    {222,252,252},
    {164,4,0},
    {53,0,0},
    {0,209,0},
    {0,64,0},
    {185,177,0},
    {61,48,0},
    {180,93,0},
    {74,20,0},
};

static const int spiral[16] = {0,1,2,3,4,11,12,13,14,15,8,7,6,5,10,9};
static const int colors[16][3] = {
    {0xff, 0x00, 0x00},
    {0xff, 0x08, 0x00},
    {0xff, 0xff, 0x00},
    {0x80, 0xff, 0x00},
    {0x00, 0xff, 0x00},
    {0x00, 0xff, 0x80},
    {0x00, 0xff, 0xff},
    {0x00, 0x80, 0xff},
    {0x00, 0x00, 0xff},
    {0x80, 0x00, 0xff},
    {0xff, 0x00, 0xff},
    {0xff, 0x00, 0x80},
    {0xff, 0xff, 0xff},
    {0xc0, 0xc0, 0xc0},
    {0x07, 0x07, 0x07},
    {0x05, 0x05, 0x05}
};

static const int pinout[16] = {2,3,4,18,6,7,8,9,10,11,12,13,14,15,17,16};
static const int remap[16]  = {0,1,2,3,7,6,5,4,8,9,10,11,15,14,13,12};

static const int logo[4][16]={
    {
        1,1,1,0,
        1,0,1,0,
        1,1,0,0,
        1,0,1,0
    },
    {
        1,0,0,0,
        1,1,1,0,
        1,0,1,0,
        1,1,1,0
    },
    {
        1,1,1,1,
        1,0,0,1,
        1,0,0,1,
        1,1,1,1
    },
    {
        1,0,0,1,
        0,1,1,0,
        0,1,1,0,
        1,0,0,1
    }
};

void intro()
{
    for(int i = 0; i < 4; i++){
        for(int lum = 30; lum >= 0; lum--){
            for(int j = 0; j < 16; j++){
                if(logo[i][j] == 1)
                    set_pixel(remap[j], lum, lum, lum);
                else
                    set_pixel(remap[j], 0, 0, 0);
            }
            sleep_ms(15);
        }
    }
    set_pixel(12,0,255,255);
    sleep_ms(10);
}

void callback(int gpio, uint32_t events)
{
    for(int i = 0; i < 16; i++){
        if(pinout[i] == gpio)
        {
            putchar(i);
            fflush(stdout);
        }
    }
    gpio_set_irq_enabled_with_callback(gpio, GPIO_IRQ_EDGE_FALL, false, &callback);
    for(int i = 0; i < 100; i++){
        asm("NOP");
    }
    gpio_set_irq_enabled_with_callback(gpio, GPIO_IRQ_EDGE_FALL, true, &callback);
}

void rboxcontrol()
{
    while (1)
    {
        char input[6];
        memset(input, 0, sizeof(input));
        for(int i = 0; i < 6; i++)
        {
            input[i] = getchar();
        }

        char number[3] = {input[0], input[1], '\0'};
        char index[4] = {input[3], input[4], input[5], '\0'};

        set_pixel(remap[atoi(number)], RGB[atoi(index)][0], RGB[atoi(index)][1],RGB[atoi(index)][2]);
        sleep_ms(1);
    }
}

void rboxtilt()
{
    while(1){
        for(int i = 0; i < 4; i++){
            for(int i = 0; i < sizeof(spiral) / sizeof(spiral[0]); i++){
                set_pixel(spiral[i], colors[i][0], colors[i][1],colors[i][2]);
                sleep_ms(50);
            }

            sleep_ms(200);

            for(int i = 0; i < sizeof(spiral) / sizeof(spiral[0]); i++){
                set_pixel(spiral[i], 0,0,0);
                sleep_ms(50);
            }
        }

        sleep_ms(200);

        for(int i = 0; i < 360; i++)
        {
            for(int j = 0; j < 16; j++){
                set_pixel(j,
                    sins[i],
                    sins[(i+120)%360],
                    sins[(i+240)%360]
                );
            }
            sleep_ms(100);
        }
    }
}

void attach_interrupts(){
    for(int gpio = 0; gpio < 16; gpio++)
    {
        gpio_pull_up(pinout[gpio]);
        gpio_set_irq_enabled_with_callback(pinout[gpio], GPIO_IRQ_EDGE_FALL, true, &callback);
    }
}
