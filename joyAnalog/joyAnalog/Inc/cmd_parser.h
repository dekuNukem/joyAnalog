#ifndef __CMD_PARSER_H
#define __CMD_PARSER_H

#ifdef __cplusplus
 extern "C" {
#endif 

#include "stm32f0xx_hal.h"
#include "main.h"
#include "helpers.h"
#include "shared.h"
#include "eeprom.h"
#include "jc_ctrl.h"

#define ACTION_RELEASE 1
#define ACTION_HOLD 0
#define ARG_PARSE_SUCCESS 0
#define ARG_PARSE_ERROR_INVALID_CMD 126
#define ARG_PARSE_ERROR_NOT_AVAILABLE 127

void parse_cmd(char* cmd);

#ifdef __cplusplus
}
#endif

#endif



/*

joycon button mapping

a
b
x
y
l
r
zl
zr
du
dd
dl
dr
sl
sr
syncl
syncr
+
-
h
cap
lsb
rsb



*/
