#ifndef __ANALOG_SWITCH_H
#define __ANALOG_SWITCH_H

#ifdef __cplusplus
 extern "C" {
#endif 

#include "stm32f0xx_hal.h"
#include "helpers.h"
#include "shared.h"

extern uint16_t button_status;

void jc_ctrl_init(void);
void button_write(uint16_t value);
void dac_write(uint8_t x_8b, uint8_t y_8b);
void stick_release(void);
void stick_disengage(void);
void release_all_button(void);

#ifdef __cplusplus
}
#endif

#endif
