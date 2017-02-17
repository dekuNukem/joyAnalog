#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define	SB_A 0
#define SB_B 1
#define SB_X 2
#define SB_Y 3
#define SB_UP 4
#define SB_DOWN 5
#define SB_LEFT 6
#define SB_RIGHT 7
#define SB_L 8
#define SB_R 9
#define SB_ZL 10
#define SB_ZR 11
#define SB_SL 12
#define SB_SR 13
#define SB_SBL 14
#define SB_SBR 15
#define SB_SYNCL 16
#define SB_SYNCR 17
#define SB_PLUS 18
#define SB_MINUS 19
#define SB_HOME 20
#define SB_CAPTURE 21

#define INPUT_BUF_SIZE 256
char input_buf[INPUT_BUF_SIZE];

#define ARG_BUF_SIZE 32
uint8_t arg_buf[ARG_BUF_SIZE];

// gcc -o blah cmd_parse.c 

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

void parse_cmd(char* cmd)
{
  if(cmd == NULL)
    return;

  if(strncmp(cmd, "test\n", 5) == 0)
    puts("test OK");
  else if(strncmp(cmd, "bh ", 3) == 0)
  {
  	char* arg_ptr = cmd;
  	int32_t count = 0;
  	while(1)
  	{
  		arg_ptr = goto_next_arg(arg_ptr);
  		if(arg_ptr == NULL)
  			break;
  		printf("%s\n", arg_ptr);
  		count++;
  	}
  	goto_next_arg(cmd);
    puts("bh OK");
  }
  else
    puts("ERROR");
}

int main()
{
	memset(input_buf, 0, INPUT_BUF_SIZE);
	sprintf(input_buf, "bh a    b  cap y");
	parse_cmd(input_buf);
	return 0;
}