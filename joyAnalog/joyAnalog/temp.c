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
    