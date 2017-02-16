#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "main.h"
#include "helpers.h"
#include "shared.h"
#include "cmd_parser.h"

#define ARG_QUEUE_SIZE 32

uint8_t arg_queue[ARG_QUEUE_SIZE];

void parse_cmd(char* cmd)
{
  if(cmd == NULL)
    return;

  if(strncmp(cmd, "test\n", 5) == 0)
    puts("test OK");
  else if(strncmp(cmd, "bh\n", 3) == 0)
  {
    puts("bh OK");
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
  }
  else if(strncmp(cmd, "br\n", 3) == 0)
  {
    puts("br OK");
    HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
  }
  else
    puts("ERROR");
}

  