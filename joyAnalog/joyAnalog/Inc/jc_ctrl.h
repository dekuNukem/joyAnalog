#ifndef __ANALOG_SWITCH_H
#define __ANALOG_SWITCH_H

#ifdef __cplusplus
 extern "C" {
#endif 

#include "stm32f0xx_hal.h"
#include "helpers.h"
#include "shared.h"


void jc_ctrl_init(void);
void button_write(uint16_t value);

#ifdef __cplusplus
}
#endif

#endif
