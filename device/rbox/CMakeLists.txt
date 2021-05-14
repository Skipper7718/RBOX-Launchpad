cmake_minimum_required(VERSION 3.12)

include(pico_sdk_import.cmake)

project(rbox C CXX ASM)

pico_sdk_init()

file(GLOB source_files
                    "src/*.c"
)

add_executable(rbox ${source_files})

pico_generate_pio_header(rbox ${CMAKE_CURRENT_LIST_DIR}/ws2812.pio)

target_link_libraries(rbox pico_stdlib hardware_pio pico_multicore hardware_gpio pico_bootrom)

pico_enable_stdio_usb(rbox 1)

pico_add_extra_outputs(rbox)

