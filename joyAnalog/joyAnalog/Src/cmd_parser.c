#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "cmd_parser.h"

char* goto_next_arg(char* buf)
{
  char* curr = buf;
  if(curr == NULL)
    return NULL;
  char* buf_end = curr + strlen(curr);
  if(curr >= buf_end)
    return NULL;
  while(curr < buf_end && *curr != ' ')
      curr++;
  while(curr < buf_end && *curr == ' ')
      curr++;
  if(curr >= buf_end)
    return NULL;
  return curr;
}

int32_t arg_to_button_index(char* cmd)
{
  int32_t result;
  if(strncmp(cmd, "dd", 2) == 0)
    result = 8;
  else if(strncmp(cmd, "du", 2) == 0)
    result = 9;
  else if(strncmp(cmd, "dr", 2) == 0)
    result = 10;
  else if(strncmp(cmd, "dl", 2) == 0)
    result = 11;
  else if(strncmp(cmd, "lsr", 3) == 0)
    result = 12;
  else if(strncmp(cmd, "lsl", 3) == 0)
    result = 13;
  else if(strncmp(cmd, "ls", 2) == 0)
    result = 14;
  else if(strncmp(cmd, "zl", 2) == 0)
    result = 15;
  else if(strncmp(cmd, "-", 1) == 0)
    result = 4;
  else if(strncmp(cmd, "sbl", 3) == 0)
    result = 5;
  else if(strncmp(cmd, "cap", 3) == 0)
    result = 6;
  else if(strncmp(cmd, "syncl", 5) == 0)
    result = 7;
  
  else if(strncmp(cmd, "y", 1) == 0)
    result = 8 + 12;
  else if(strncmp(cmd, "x", 1) == 0)
    result = 9 + 12;
  else if(strncmp(cmd, "b", 1) == 0)
    result = 10 + 12;
  else if(strncmp(cmd, "a", 1) == 0)
    result = 11 + 12;
  else if(strncmp(cmd, "rsr", 3) == 0)
    result = 12 + 12;
  else if(strncmp(cmd, "rsl", 3) == 0)
    result = 13 + 12;
  else if(strncmp(cmd, "rs", 2) == 0)
    result = 14 + 12;
  else if(strncmp(cmd, "zr", 2) == 0)
    result = 15 + 12;
  else if(strncmp(cmd, "+", 1) == 0)
    result = 4 + 12;
  else if(strncmp(cmd, "sbr", 3) == 0)
    result = 5 + 12;
  else if(strncmp(cmd, "h", 1) == 0)
    result = 6 + 12;
  else if(strncmp(cmd, "syncr", 5) == 0)
    result = 7 + 12;
  else
    return ARG_PARSE_ERROR_INVALID_CMD;

  if((board_type == BOARD_TYPE_NDAC_MINI_JOYCON_LEFT && result >= 4 && result <= 15) ||
    (board_type == BOARD_TYPE_NDAC_MINI_JOYCON_RIGHT && result >= 16 && result <= 27))
    return result;
  return ARG_PARSE_ERROR_NOT_AVAILABLE;
}

int32_t process_multiarg(char* args, uint8_t action)
{
  char* arg_ptr = args;
  while(arg_ptr != NULL)
  {
    int32_t result = arg_to_button_index(arg_ptr);
    if(result >= 4 && result <= 27)
    {
    	result > 15 ? result -= 12 : result;
    	if(action == ACTION_HOLD)
    		SetBit(button_status, result);
    	else
    		ClearBit(button_status, result);
    }
    else
      return result;
    arg_ptr = goto_next_arg(arg_ptr);
  }
  button_write(button_status);
  return ARG_PARSE_SUCCESS;
}

int32_t stick_hold(char* cmd)
{
  char* x_ptr = goto_next_arg(cmd);
  char* y_ptr = goto_next_arg(x_ptr);
  uint32_t x_8b = atoi(x_ptr);
  uint32_t y_8b = atoi(y_ptr);
  if(x_ptr == NULL || y_ptr == NULL || x_8b > 255 || y_8b > 255)
    return ARG_PARSE_ERROR_INVALID_CMD;
  dac_write(x_8b, y_8b);
  return ARG_PARSE_SUCCESS;
}

int32_t tas_parse(char* cmd)
{
  char* arg_ptr = goto_next_arg(cmd);
  int32_t arg_pos = 0;
  int32_t xxx = 127;
  int32_t yyy = 127;
  while(arg_ptr != NULL)
  {
    if(arg_pos == 2)
      xxx = atoi(arg_ptr);
    else if(arg_pos == 3)
      yyy = atoi(arg_ptr);
    else if(arg_pos >= 4)
    {
      if(atoi(arg_ptr))
        SetBit(button_status, arg_pos);
      else
        ClearBit(button_status, arg_pos);
    }
    arg_pos++;
    arg_ptr = goto_next_arg(arg_ptr);
  }
  button_write(button_status);
  dac_write(xxx, yyy);
  return ARG_PARSE_SUCCESS;
}

void parse_cmd(char* cmd)
{
  int32_t result;
  if(strcmp(cmd, "test") == 0)
    puts("test OK");
  else if(strncmp(cmd, "tas ", 4) == 0)
  {
    tas_parse(cmd);
    puts("tas OK");
  }
  else if(strcmp(cmd, "eepinit") == 0)
  {
    eeprom_erase();
    eeprom_write(EEPROM_BOARD_TYPE_ADDR, BOARD_TYPE_NDAC_MINI_JOYCON_LEFT);
    board_type = BOARD_TYPE_NDAC_MINI_JOYCON_LEFT;
    puts("eepinit OK");
  }
  else if(strncmp(cmd, "settype l", 9) == 0)
  {
    eeprom_write(EEPROM_BOARD_TYPE_ADDR, BOARD_TYPE_NDAC_MINI_JOYCON_LEFT);
    board_type = BOARD_TYPE_NDAC_MINI_JOYCON_LEFT;
    printf("settype OK\n");
  }
  else if(strncmp(cmd, "settype r", 9) == 0)
  {
    eeprom_write(EEPROM_BOARD_TYPE_ADDR, BOARD_TYPE_NDAC_MINI_JOYCON_RIGHT);
    board_type = BOARD_TYPE_NDAC_MINI_JOYCON_RIGHT;
    printf("settype OK\n");
  }
  else if(strcmp(cmd, "whoami") == 0)
  {
    board_type = eeprom_read(EEPROM_BOARD_TYPE_ADDR);
    switch(board_type)
    {
      case BOARD_TYPE_NDAC_MINI_JOYCON_LEFT:
      puts("BOARD_TYPE_NDAC_MINI_JOYCON_LEFT");
      break;

      case BOARD_TYPE_NDAC_MINI_JOYCON_RIGHT:
      puts("BOARD_TYPE_NDAC_MINI_JOYCON_RIGHT");
      break;

      default:
      puts("unknown board type, use 'settype l/r' to configure this board");
      break;
    }
  }
  // button hold, multiple args allowed
  else if(strncmp(cmd, "bh ", 3) == 0)
  {
    result = process_multiarg(goto_next_arg(cmd), ACTION_HOLD);
    switch(result)
    {
      case ARG_PARSE_SUCCESS:
      puts("bh OK");
      break;
      case ARG_PARSE_ERROR_INVALID_CMD:
      puts("bh ERROR: invalid command");
      break;
      case ARG_PARSE_ERROR_NOT_AVAILABLE:
      puts("bh ERROR: not available on this side");
      break;
      default:
      puts("bh ERROR: unknown");
    }
  }
  // button release, multiple args allowed
  else if(strncmp(cmd, "br ", 3) == 0)
  {
    result = process_multiarg(goto_next_arg(cmd), ACTION_RELEASE);
    switch(result)
    {
      case ARG_PARSE_SUCCESS:
      puts("br OK");
      break;
      case ARG_PARSE_ERROR_INVALID_CMD:
      puts("br ERROR: invalid command");
      break;
      case ARG_PARSE_ERROR_NOT_AVAILABLE:
      puts("br ERROR: not available on this side");
      break;
      default:
      puts("br ERROR: unknown");
    }
  }
  // button release all
  else if(strcmp(cmd, "bra") == 0)
  {
    release_all_button();
    puts("bra OK");
  }
  // stick hold, sh x y, x and y between 0 and 255 inclusive
  else if(strncmp(cmd, "sh ", 3) == 0)
  {
    result = stick_hold(cmd);
    switch(result)
    {
      case ARG_PARSE_SUCCESS:
      puts("sh OK");
      break;
      case ARG_PARSE_ERROR_INVALID_CMD:
      puts("sh ERROR: invalid command");
      break;
      default:
      puts("sh ERROR: unknown");
    }
  }
  // stick release, to netural position 
  else if(strcmp(cmd, "sr") == 0)
  {
    stick_release();
    puts("sr OK");
  }
  // stick disengage, gives control back to user
  else if(strcmp(cmd, "sd") == 0)
  {
    stick_disengage();
    puts("sd OK");
  }
  // release all buttons and sticks
  else if(strcmp(cmd, "reset") == 0)
  {
    release_all_button();
    stick_release();
    puts("reset OK");
  }
  else
  {
    puts("ERROR unknown command");
  }
  // printf("button_status: %x\n", button_status);
}
