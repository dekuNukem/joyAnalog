## NintenDAC

This is the bigger board that could be used on modifying the pro controller, or the console itself. It has more GPIOs than the mini, and has 10 channels of high speed DAC output.

![Alt text](http://i.imgur.com/ir8jZFO.jpg)

* 48MHz STM32F072R8T6 microcontroller, 64KB flash, 16KB RAM.
* MAX5723/MAX5724/MAX5725 8-channel high-speed SPI DAC + 2-channel built-in DAC.
* 1KB I2C EEPROM, user button, user LED.
* 36 GPIOs(or 40 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 4.1 x 4.1 cm, or 1.65 x 1.65 inch.

## Command protocol

NintenDAC uses a simple serial command protocol. To use it open the port at any baud rate, then send a command in ASCII string. The board will send a respond back.

Commands should be in lower case, and end with a single `\n`.

### Commands

**command**|**arguments**|**remark**|**response**|**example**
:-----:|:-----:|:-----:|:-----:|:-----:
`eepinit`|none|initializes EEPROM to default value|`eepinit OK`|`eepinit`
`settype`|l / r|set this board as left or right Joycon|`settype OK`|`settype l`
`whoami`|none|see which side is this board|A string containing `LEFT` or `RIGHT`; `unknown` if incorrectly set up|`whoami`
`bh`|button args (see below)|hold button|`bh OK` if no error; `ERROR`  otherwise|`bh a b x`
`br`|button args (see below)|release button|`br OK` if no error; `ERROR` otherwise|`br a b x`
`bra`|none|release all buttons on this board|`bra OK`|`bra`
`reset`|none|release all buttons as well as disengage the stick|`reset OK`|`reset`

---under construction---under construction---

### Button args

**arg**|**button**
:-----:|:-----:
`du`|D-pad up
`dd`|D-pad down
`dl`|D-pad left
`dr`|D-pad right
`ls`|L button
`zl`|ZL button
`-`|minus button 
`cap`|capture button
`sbl`|left stick button
`a`|A button
`b`|B button
`x`|X button
`y`|Y button
`rs`|R button
`zr`|ZR button
`+`|plus button
`h`|home button
`sbr`|right stick button
`sync`|SYNC button

### A few words about commands

* `sh` and `sr` will take over the control stick, meaning the input won't change when you move the stick with your finger when those commands are active. To get back to manual control use `sd`

* `bh` and `br` can have one or multiple arguments, as long as they are all valid. So you can have `bh a` or `bh a b x y zr h +` etc. The max number of arguments is 16.

---under construction---under construction---

