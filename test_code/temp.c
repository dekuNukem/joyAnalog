HAL_DAC_DeInit(stm32_dac_ptr);

// max dac
void test(void)
{
  max572x_POWER(0x3, max572x_POWER_NORMAL);
  printf("run started\n");
  uint16_t count = 0;
  while(1)
  {
    max572x_CODEn_LOADn(0, count);
    max572x_CODEn_LOADn(1, ~count);
    count++;
  }
}

// bulit in dac
void test(void)
{
  printf("run started\n");
  uint16_t count = 0;
  while(1)
  {
    // HAL_DAC_SetValue(stm32_dac_ptr, DAC_CHANNEL_1, DAC_ALIGN_8B_R, count);
    // HAL_DACEx_DualSetValue(stm32_dac_ptr, DAC_ALIGN_8B_R, count, 255 - count);
    HAL_DACEx_DualSetValue(stm32_dac_ptr, DAC_ALIGN_12B_R, count, 65535 - count);
    count++;
  }
}


if(linear_buf_line_available(&debug_lb))
		{
		  printf("debug_lb: %s\n", debug_lb.buf);

		  if(strstr(debug_lb.buf, "s ") != NULL)
		  {
		  	uint8_t to_send = get_arg(debug_lb.buf, 0);
		  	uint8_t received = 0;
		  	printf("sending %d...\n", to_send);
		  	spi_cs_low();
		  	HAL_SPI_TransmitReceive(max572x_spi_ptr, &to_send, &received, 1, 500);
		  	spi_cs_high();
		  	printf("received: %d\n", received);
		  }
		  linear_buf_reset(&debug_lb);
		}


  SPI2_CS_GPIO_Port->ODR |= 0x1000; // CS high
  SPI2_CS_GPIO_Port->ODR &= 0xefff; // CS low


void max572x_POWER(uint8_t dac_multi_sel, uint8_t power_mode)
{
  uint8_t power = (uint8_t)((power_mode << 6) & 0xc0);
  printf("power: 0x%X\n", power);
  // uint8_t to_send[3] = {0x40, dac_multi_sel, (power_mode << 6) & 0xc0};
}

  printf("sending 0x%X 0x%X 0x%X...\n", to_send[0], to_send[1], to_send[2]);
void max572x_POWER(uint8_t dac_multi_sel, uint8_t power_mode)
{
  uint8_t to_send[3] = {0x40, dac_multi_sel, (uint8_t)((power_mode << 6) & 0xc0)};
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, to_send, 3, 100);
  spi_cs_high();
}

void read_status()
{
  uint8_t spi_sb[3] = {0xe8, 0xaa, 0xaa};
  uint8_t spi_rb[3] = {0, 0, 0};
  printf("sending 0x%X 0x%X 0x%X...\n", spi_sb[0], spi_sb[1], spi_sb[2]);
  spi_cs_low();
  HAL_SPI_TransmitReceive(max572x_spi_ptr, spi_sb, spi_rb, 3, 500);
  spi_cs_high();
  printf("spi_rb: 0x%X 0x%X 0x%X\n", spi_rb[0], spi_rb[1], spi_rb[2]);
}

void read_status()
{
  uint8_t spi_sb[3] = {0xe8, 0xaa, 0xaa};
  uint8_t spi_rb[3] = {0, 0, 0};
  printf("sending: ");
  print_3b(spi_sb);
  spi_cs_low();
  HAL_SPI_TransmitReceive(max572x_spi_ptr, spi_sb, spi_rb, 3, 500);
  spi_cs_high();
  printf("received: ");
  print_3b(spi_rb);
}

void max5725_CODEn(uint8_t dac_sel, uint16_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  data &= 0xfff;
  spi_sb[1] |= data >> 4;
  data &= 0xf;
  spi_sb[2] |= (data << 4);
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5725_CODEn: "); print_3b(spi_sb);
}

void max5723_CODEn(uint8_t dac_sel, uint8_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  spi_sb[1] = data;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5723_CODEn: "); print_3b(spi_sb);
}

void pack_dac_val(uint8_t part, uint16_t value, uint8_t* dh, uint8_t* dl)
{
  if(part == MAX5723)
    *dh = (value & 0xff);
  else if(part == MAX5724)
  {
    value &= 0x3ff;
    *dh |= value >> 2;
    value &= 0x3;
    *dl |= (value << 6);
  }
  else
  {
    value &= 0xfff;
    *dh |= value >> 4;
    value &= 0xf;
    *dl |= (value << 4);
  }
}


void max5723_CODEn(uint8_t dac_sel, uint8_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  spi_sb[1] = data;
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5723_CODEn: "); print_3b(spi_sb);
}

void max5724_CODEn(uint8_t dac_sel, uint16_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  data &= 0x3ff;
  spi_sb[1] |= data >> 2;
  data &= 0x3;
  spi_sb[2] |= (data << 6);
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5724_CODEn: "); print_3b(spi_sb);
}

void max5725_CODEn(uint8_t dac_sel, uint16_t data)
{
  uint8_t spi_sb[3] = {0x80, 0, 0};
  dac_sel &= 0xf;
  spi_sb[0] |= dac_sel;
  data &= 0xfff;
  spi_sb[1] |= data >> 4;
  data &= 0xf;
  spi_sb[2] |= (data << 4);
  spi_cs_low();
  HAL_SPI_Transmit(max572x_spi_ptr, spi_sb, 3, 100);
  spi_cs_high();
  // printf("max5725_CODEn: "); print_3b(spi_sb);
}

// printf("max572x_SW_RESET\n");
// printf("max572x_POWER: "); print_3b(spi_sb);
// printf("max572x_CONFIG: "); print_3b(spi_sb);
// printf("max572x_WDOG: "); print_3b(spi_sb);
// printf("max572x_REF: "); print_3b(spi_sb);
// printf("max572x_CODEn: "); print_3b(spi_sb);
// printf("max572x_LOADn: "); print_3b(spi_sb);

void print_3b(uint8_t buf[3])
{
  printf("0x%x 0x%x 0x%x\n", buf[0], buf[1], buf[2]);
}

#define MAX5723 0
#define MAX5724 1
#define MAX5725 2

int fputc(int ch, FILE *f)
{
    HAL_UART_Transmit(&huart1, (unsigned char *)&ch, 1, 100);
    return ch;
}
while (1)
  {
    HAL_UART_Receive_IT(&huart1, debug_byte_buf, 1);
  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */
    if(linear_buf_line_available(&debug_lb))
    {
      printf("debug_lb: %s\n", debug_lb.buf);
      test();
      linear_buf_reset(&debug_lb);
    }
  }

  while(1)
  {
    usb_data = my_usb_readline();
    if(usb_data != NULL)
    {
      printf("I received: %s\n", usb_data);
    }
  }

uint8_t debug_byte_buf[1];
linear_buf debug_lb;
extern UART_HandleTypeDef huart1;
#define debug_uart_ptr (&huart1)
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  if(huart->Instance==USART1)
  {
      linear_buf_add(&debug_lb, debug_byte_buf[0]);
      HAL_UART_Receive_IT(&huart1, debug_byte_buf, 1);
  }
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *huart)
{
  if(huart->Instance==USART1)
  {
      HAL_UART_Receive_IT(&huart1, debug_byte_buf, 1);
      linear_buf_reset(&debug_lb);
  }
}
      HAL_GPIO_TogglePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin);