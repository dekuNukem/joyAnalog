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
`whoami`|none|see which side is this board for|"A string containing `LEFT` or `RIGHT`; `unknown` if incorrectly set up"|`whoami`
`bh`|one or more button args|hold down button|`bh OK` if no error; `ERROR`  otherwise|`bh a b x`
`br`|one or more button args|release button|`br OK` if no error; `ERROR` otherwise|`br a b x`
`bra`|none|release all buttons on this board|`bra ok`|`bra`

under construction...

## NintenDAC Python library

under construction...
