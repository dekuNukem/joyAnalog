idwg_kick();
    usb_data = my_usb_readline();
    if(usb_data != NULL)
      parse_cmd(usb_data); 

  while (1)
  {
  /* USER CODE END WHILE */

  /* USER CODE BEGIN 3 */
    idwg_kick();
    usb_data = my_usb_readline();
    if(usb_data != NULL)
      parse_cmd(usb_data); 
  }

if(HAL_GPIO_ReadPin(USER_BUTTON_GPIO_Port, USER_BUTTON_Pin) == GPIO_PIN_RESET)
    {
      HAL_GPIO_WritePin(KEYPAD_COL1_GPIO_Port, KEYPAD_COL1_Pin, GPIO_PIN_RESET);
      HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_RESET);
      delay_us(1215);
      HAL_GPIO_WritePin(KEYPAD_COL1_GPIO_Port, KEYPAD_COL1_Pin, GPIO_PIN_SET);
      HAL_GPIO_WritePin(DEBUG_LED_GPIO_Port, DEBUG_LED_Pin, GPIO_PIN_SET);
      HAL_Delay(1000);
    }