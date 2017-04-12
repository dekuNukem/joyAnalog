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


void dac_write(uint8_t x_8b, uint8_t y_8b)
{
  uint32_t x_12b = (uint32_t)((float)x_8b * 8.76);
  uint32_t y_12b = (uint32_t)((float)y_8b * 8.76);
  if(dac_ptr->State == HAL_DAC_STATE_RESET)
    stm32_dac_init();
  HAL_DACEx_DualSetValue(dac_ptr, DAC_ALIGN_12B_R, x_12b, y_12b);
}

void stick_release(void)
{
  if(dac_ptr->State == HAL_DAC_STATE_RESET)
    stm32_dac_init();
  HAL_DACEx_DualSetValue(dac_ptr, DAC_ALIGN_12B_R, 1117, 1117);
}

void stick_disengage(void)
{
  if(dac_ptr->State != HAL_DAC_STATE_RESET)
  {
    HAL_DAC_Stop(dac_ptr, DAC_CHANNEL_1);
    HAL_DAC_Stop(dac_ptr, DAC_CHANNEL_2);
    HAL_DAC_DeInit(dac_ptr);
  }
}

void release_all_button(void)
{
	button_status = 0;
	button_write(button_status);
}
