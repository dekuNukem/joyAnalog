## NintenDAC mini

![Alt text](http://i.imgur.com/f3qcFR7.jpg)

* 48MHz STM32F072C8T6 microcontroller, 64KB flash, 16KB RAM.
* Built-in 2-channel 12-bit DAC.
* 1KB I2C EEPROM, user button, user LED.
* 28 GPIOs(or 32 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 2.5 x 4.1 cm, 1 x 1.6 inch.

## NintenDAC mini serial command protocol

NintenDAC mini uses a simple serial command protocol. To use it open the port at any baud rate(it doesn't matter because it's USB based), then send a ASCII command string terminated with `\n` and the board will send a response back.

valid commands are:

under construction...

## NintenDAC Python library

I also wrote a simple python3 library for NintenDAC mini, an example is provided, and I'll finish up the documentation in the coming days.

## Twitch Plays Nintendo Switch

I dug up and reused a portion of my old code for TwitchPlaysPokemonX.

