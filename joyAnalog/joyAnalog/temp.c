void my_usb_putchar(uint8_t ch)
{
  if(port_opened == 0)
      return;
  int32_t start = HAL_GetTick();
  while(1)
  {
    uint8_t result = CDC_Transmit_FS(&ch, 1);
    if(result == USBD_OK || result == USBD_FAIL)
      return;
    if(HAL_GetTick() - start > 100)
    {
      port_opened = 0;
      return;
    }
    if(result == USBD_BUSY)
      continue;
  }
}

    HAL_GPIO_TogglePin(USER_LED_GPIO_Port, USER_LED_Pin);
    printf("hello world\n");
    spi_cs_low();
    HAL_SPI_Transmit(spi1_ptr, spi_sb, 2, 100);
    spi_cs_high();

    HAL_Delay(200);


// uint8_t spi_sb[2] = {0xab, 0xcd};
  // second byte controls first in chain
  uint8_t spi_sb[2] = {0x40, 0x6};

  printf("%s\n", usb_data);

  usb_data = my_usb_readline();
    if(usb_data != NULL)
    {
        for (int i = 0; i < 32; ++i)
          printf("%d: %d\n", i, eeprom_read(i));
    }

  printf("%x %x %x\n", value, array[1], array[0]);
    
void button_ctrl(GPIO_PinState action)
{
  for(int i = 0; i < ARG_QUEUE_SIZE; ++i)
    if(gpio_port_queue[i] != NULL)
      HAL_GPIO_WritePin(gpio_port_queue[i], gpio_pin_queue[i], action);
}
int32_t button_hold(char* cmd)
{
  char* arg_start = goto_next_arg(cmd);
  int32_t result = process_multiarg(arg_start);
  if(result == ARG_PARSE_SUCCESS)
    button_ctrl(GPIO_PIN_RESET);
  return result;
}

int32_t button_release(char* cmd)
{
  char* arg_start = goto_next_arg(cmd);
  int32_t result = process_multiarg(arg_start);
  if(result == ARG_PARSE_SUCCESS)
    button_ctrl(GPIO_PIN_SET);
  return result;
}
int32_t button_hold(char* cmd)
{
  char* arg_start = goto_next_arg(cmd);
  int32_t result = process_multiarg(arg_start);
  if(result == ARG_PARSE_SUCCESS)
    button_ctrl(GPIO_PIN_RESET);
  return result;
}

int32_t button_release(char* cmd)
{
  char* arg_start = goto_next_arg(cmd);
  int32_t result = process_multiarg(arg_start);
  if(result == ARG_PARSE_SUCCESS)
    button_ctrl(GPIO_PIN_SET);
  return result;
}

/*
import joyanalog

switch = joyanalog.joyanalog("COM5", "COM4")
switch.connect()

# give it a list of valid button args
# switch.button_hold(['a', 'b', 'zl', 'zr'])
# switch.button_release(['a'])
# switch.button_release_all()

# press button(s) then release it
# first arg is how long to press the button(s) down
# second arg is how long to release them before the next action
# value smaller than 33ms (1 frame) probably won't get recognized by the console
# third arg is the list of buttons
switch.button_click(100, 100, ['a'])
switch.button_click(100, 100, ['b'])
switch.button_click(100, 100, ['x'])
switch.button_click(100, 100, ['y'])

# first arg is which stick to hold, should be 'l' or 'r'
# second and third arg are desired stick position
# must between 0 to 255 inclusive, 127 is netural postion
switch.stick_hold('l', 64, 192)
switch.stick_release('r')

# give back stick control to user
switch.stick_disengage('l')

# hold the stick to a position then release it
# first arg is which side, should be 'l' or 'r'
# second arg is how long to hold the stick
# third arg is how long to release the stick before the next action
# fourth and fifth arg are stick position x and y
switch.stick_nudge('l', 67, 67, 192, 168)

# release all buttons and disengage all sticks
switch.reset()

switch.disconnect()

*/

if(value & 0x40)
      HAL_GPIO_WritePin(STICK_BUTTON_GPIO_Port, STICK_BUTTON_Pin, GPIO_PIN_RESET);
    else
      HAL_GPIO_WritePin(STICK_BUTTON_GPIO_Port, STICK_BUTTON_Pin, GPIO_PIN_SET);