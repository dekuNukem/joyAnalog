#ifndef __MAX572X_H
#define __MAX572X_H

#ifdef __cplusplus
 extern "C" {
#endif 

#include "stm32f0xx_hal.h"
#include "shared.h"

#define max572x_POWER_NORMAL 0x0
#define max572x_POWER_1K 0x40
#define max572x_POWER_100K 0x80
#define max572x_POWER_HIZ 0xc0

#define max572x_CONFIG_WDOG_DISABLE 0x0
#define max572x_CONFIG_WDOG_GATE 0x40
#define max572x_CONFIG_WDOG_CLR 0x80
#define max572x_CONFIG_WDOG_HOLD 0xc0
#define max572x_CONFIG_GATE_EN 0x20
#define max572x_CONFIG_LDAC_EN 0x10
#define max572x_CONFIG_CLR_EN 0x8

#define max572x_WDOG_WD_MASK 0x8
#define max572x_WDOG_SAFETY_LOW 0x0
#define max572x_WDOG_SAFETY_MID 0x2
#define max572x_WDOG_SAFETY_HIGH 0x4
#define max572x_WDOG_SAFETY_MAX 0x6

#define max572x_REF_POWER 0x4
#define max572x_REF_EXT 0x0
#define max572x_REF_2V5 0x1
#define max572x_REF_2V0 0x2
#define max572x_REF_4V0 0x3

#define MAX5723 0
#define MAX5724 1
#define MAX5725 2

void test(void);

#ifdef __cplusplus
}
#endif

#endif


