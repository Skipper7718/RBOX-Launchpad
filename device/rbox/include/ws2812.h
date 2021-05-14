#include <stdint.h>


#define STRING_LEN 16


void init_ws2812();

void ws2812b_core();

int set_pixel(int pixel_num, uint8_t r, uint8_t g, uint8_t b);

int fill_pixel(uint8_t r, uint8_t g, uint8_t b);

static inline uint32_t urgb_u32(uint8_t r, uint8_t g, uint8_t b);

static inline void put_pixel(uint32_t pixel_grb);

long map(long x, long in_min, long in_max, long out_min, long out_max);