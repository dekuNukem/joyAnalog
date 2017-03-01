## NintenDAC mini

![Alt text](http://i.imgur.com/f3qcFR7.jpg)

* 48MHz STM32F072C8T6 microcontroller, 64KB flash, 16KB RAM.
* Built-in 2-channel 12-bit DAC.
* 1KB I2C EEPROM, user button, user LED.
* 28 GPIOs(or 32 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 2.5 x 4.1 cm, 1 x 1.6 inch.

## Command protocol

NintenDAC mini uses a simple serial command protocol. To use it open the port at any baud rate, then send a ASCII command string terminated with `\n` and the board will send a respond back.

Valid commands are:

**command**|**arguments**|**remark**|**response**|**example**
:-----:|:-----:|:-----:|:-----:|:-----:
`eepinit`|none|initializes EEPROM to default value|`eepinit OK`|`eepinit`
`settype`|l / r|set this board as left or right joycon|`settype OK`|`settype l`
`whoami`|none|see which side is this board|A string containing `LEFT` or `RIGHT`; `unknown` if incorrectly set up|`whoami`
`bh`|one or more button args|hold button|`bh OK` if no error; `ERROR`  otherwise|`bh a b x`
`br`|one or more button args|release button|`br OK` if no error; `ERROR` otherwise|`br a b x`
`bra`|none|release all buttons on this board|`bra OK`|`bra`
`sh`|x and y value|move stick to x and y value; x y should be between 0 and 255 inclusive; 127 is netural position|`bh OK`|`sh 127 245`
`sr`|none|move stick back to netural position|`br OK`|`sr`
`sd`|none|stick disengage; give physical stick control back to user|`sd OK`|`sd`
`reset`|none|release all buttons; as well as disengage the stick|`reset OK`|`reset`

under construction...

## NintenDAC Python library

under construction...
