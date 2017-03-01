### STM32 development boards with up to 10 high-speed 12-bit DAC channels.

I intend to use it for automating Nintendo Switch joycon inputs, but it can also be used as a general purpose dev board. 

There are 2 versions of NintenDac board, the bigger NintenDAC:

![Alt text](http://i.imgur.com/ir8jZFO.jpg)

* 48MHz STM32F072R8T6 microcontroller, 64KB flash, 16KB RAM.
* MAX5723/MAX5724/MAX5725 8-channel high-speed SPI DAC + 2-channel built-in DAC.
* 1KB I2C EEPROM, user button, user LED.
* 36 GPIOs(or 40 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 4.1 x 4.1 cm, or 1.65 x 1.65 inch.

And the smaller NintenDAC mini, intended to be used on a Joycon:

![Alt text](http://i.imgur.com/sMGv5oS.jpg)

* 48MHz STM32F072C8T6 microcontroller, 64KB flash, 16KB RAM.
* Built-in 2-channel 12-bit DAC.
* 1KB I2C EEPROM, user button, user LED.
* 28 GPIOs(or 32 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 2.5 x 4.1 cm, or 1 x 1.6 inch.
