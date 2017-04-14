#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "jc_ctrl.h"

uint16_t button_status;
uint16_t stick_idle_dac_val;
float dac_modifier;

// ? = 4096 * 1.2 / vcc
void jc_ctrl_init(void)
{
	button_status = 0;
	button_write(button_status);
	if(get_vref() < 1536) // 3.3v
		stick_idle_dac_val = 1120;
	else // 3.0v
		stick_idle_dac_val = 1230;
	dac_modifier = (float)stick_idle_dac_val / 127;
}

void button_write(uint16_t value)
{
	uint8_t spi_buf[2];
	spi_buf[0] = value & 0xff;
	spi_buf[1] = (value >> 8);
	spi_cs_low();
    HAL_SPI_Transmit(spi1_ptr, spi_buf, 2, 100);
    spi_cs_high();
    if(value & 0x20)
      HAL_GPIO_WritePin(STICK_BUTTON_GPIO_Port, STICK_BUTTON_Pin, GPIO_PIN_RESET);
    else
      HAL_GPIO_WritePin(STICK_BUTTON_GPIO_Port, STICK_BUTTON_Pin, GPIO_PIN_SET);

}


void dac_write(uint8_t x_8b, uint8_t y_8b)
{
  uint32_t x_12b = (uint32_t)((float)x_8b * dac_modifier);
  uint32_t y_12b = (uint32_t)((float)y_8b * dac_modifier);
  if(dac_ptr->State == HAL_DAC_STATE_RESET)
    stm32_dac_init();
  HAL_DACEx_DualSetValue(dac_ptr, DAC_ALIGN_12B_R, x_12b, y_12b);
}

void stick_release(void)
{
  if(dac_ptr->State == HAL_DAC_STATE_RESET)
    stm32_dac_init();
  HAL_DACEx_DualSetValue(dac_ptr, DAC_ALIGN_12B_R, stick_idle_dac_val, stick_idle_dac_val);
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
