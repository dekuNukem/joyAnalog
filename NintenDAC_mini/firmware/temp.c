idwg_kick();
    usb_data = my_usb_readline();
    if(usb_data != NULL)
      parse_cmd(usb_data); 