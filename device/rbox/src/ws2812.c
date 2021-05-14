#include <stdio.h>
#include <stdlib.h>

#include "../include/ws2812.h"

#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/clocks.h"
#include "ws2812.pio.h"
#include "pico/multicore.h"

int bit_depth=12;
const int PIN_TX = 0;

uint32_t pixelsb[STRING_LEN];
uint32_t errorsb[STRING_LEN];

uint32_t pixelsr[STRING_LEN];
uint32_t errorsr[STRING_LEN];

uint32_t pixelsg[STRING_LEN];
uint32_t errorsg[STRING_LEN];

long map(long x, long in_min, long in_max, long out_min, long out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

static inline void put_pixel(uint32_t pixel_grb) {
    pio_sm_put_blocking(pio0, 0, pixel_grb << 8u);
}

static inline uint32_t urgb_u32(uint8_t r, uint8_t g, uint8_t b) {
    return
            ((uint32_t) (r) << 8) |
            ((uint32_t) (g) << 16)|
            (uint32_t) (b);
}

int set_pixel(int pixel_num, uint8_t r, uint8_t g, uint8_t b)
{
	if(r + g + b <=255*3 && r + g + b >= 0 && pixel_num < STRING_LEN)
	{
		pixelsr[pixel_num] = map(r, 0, 255, 0, 20000);
		pixelsg[pixel_num] = map(g, 0, 255, 0, 20000);
		pixelsb[pixel_num] = map(b, 0, 255, 0, 20000);
		return 1;
	}
	else
		return 0;
}

int fill_pixel(uint8_t r, uint8_t g, uint8_t b)
{
	if(r + g + b <=255*3 && r + g + b >= 0)
	{
		for(int i = 0; i < STRING_LEN; i++)
		{
			pixelsr[i] = map(r, 0, 255, 0, 20000);
			pixelsg[i] = map(g, 0, 255, 0, 20000);
			pixelsb[i] = map(b, 0, 255, 0, 20000);
		}
		return 1;
	}
	else
		return 0;
}

void ws2812b_core() {
	int valuer, valueg, valueb;
	int shift = bit_depth-8;
	
    while (1){
		
		for(int i=0; i<STRING_LEN; i++) {
			valueb=(pixelsb[i] + errorsb[i]) >> shift;
			valuer=(pixelsr[i] + errorsr[i]) >> shift;
			valueg=(pixelsg[i] + errorsg[i]) >> shift;

			put_pixel(urgb_u32(valuer, valueg, valueb));
			errorsb[i] = (pixelsb[i] + errorsb[i]) - (valueb << shift); 
			errorsr[i] = (pixelsr[i] + errorsr[i]) - (valuer << shift); 
			errorsg[i] = (pixelsg[i] + errorsg[i]) - (valueg << shift); 
		}
		sleep_us(400);
	}
}

void init_ws2812()
{	
	PIO pio = pio0;
    int sm = 0;
    uint offset = pio_add_program(pio, &ws2812_program);
    ws2812_program_init(pio, sm, offset, PIN_TX, 800000, false);
	
	for(int i=0; i< STRING_LEN; ++i) {
		pixelsr[i]=0;
		pixelsg[i]=0;
		pixelsb[i]=0;
	}
 
	multicore_launch_core1(ws2812b_core);
}