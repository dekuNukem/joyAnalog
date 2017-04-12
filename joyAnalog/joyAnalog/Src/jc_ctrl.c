#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "jc_ctrl.h"

uint16_t button_status;
uint8_t analog_stick_x;
uint8_t analog_stick_y;

void jc_ctrl_init(void)
{
	button_status = 0;
	analog_stick_x = 127;
	analog_stick_y = 127;
	button_write(button_status);
}


/*
bit			button
15			B8
14			B7
13			B6
12			B5
11			B4
10			B3
9			B2
8			B1
7			B12
6			B11
5			B10
4			B9
3			unused
2			unused
1			unused
0			unused
*/
void button_write(uint16_t value)
{
	uint8_t spi_buf[2];
	spi_buf[0] = value & 0xff;
	spi_buf[1] = (value >> 8);
	spi_cs_low();
    HAL_SPI_Transmit(spi1_ptr, spi_buf, 2, 100);
    spi_cs_high();
}
