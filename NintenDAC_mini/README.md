## NintenDAC mini

This is the board that's to be used on modifying the Joycon. It's small enough to be taped to the back of each one.

![Alt text](http://i.imgur.com/f3qcFR7.jpg)

* 48MHz STM32F072C8T6 microcontroller, 64KB flash, 16KB RAM.
* Built-in 2-channel 12-bit DAC.
* 1KB I2C EEPROM, user button, user LED.
* 28 GPIOs(or 32 using internal oscillators), BOOT0, RESET, VBAT, and SWD.
* USB for power and communication, standby wakeup on USB connection.
* Board size 2.5 x 4.1 cm, 1 x 1.6 inch.

## Command protocol

NintenDAC mini uses a simple serial command protocol. To use it open the port at any baud rate, then send a command in ASCII string. The board will send a respond back.

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
`sh`|x y|move stick to x and y value. x y should be between 0 and 255 inclusive; 127 is netural position|`bh OK`|`sh 127 245`
`sr`|none|move stick back to netural position|`br OK`|`sr`
`sd`|none|stick disengage|`sd OK`|`sd`
`reset`|none|release all buttons as well as disengage the stick|`reset OK`|`reset`

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
`lsl`|left Joycon SL button
`lsr`|left Joycon SR button
`syncl`|left Joycon SYNC button
`sbl`|left Joycon stick button
`a`|A button
`b`|B burron
`x`|X button
`y`|Y button
`rs`|R button
`zr`|ZE button
`+`|plus button
`h`|home button
`rsl`|right Joycon SL button
`rsr`|right Joycon SR button
`syncr`|right Joycon SYNC button
`sbr`|right Joycon stick button

### A few words about commands

* `sh` and `sr` will take over the control stick, meaning the input won't change when you move the stick with your finger when those commands are active. To get back to manual control use `sd`

* Not all buttons are available on one board. For example if you try to `bh a` on a left Joycon board, you will get an error because there is no A button on left Joycon.

* `bh` and `br` can have one or multiple arguments, as long as they are all valid. So you can have `bh a` or `bh a b x y zr h +` etc. The max number of arguments is 16.


## NintenDAC Python3 library

I also wrote a simple python3 library so you don't have to remember all the commands above. It requires `pyserial`.

The simplest example is this:

```
import ndacmini

switch = ndacmini.ndacmini("COM4", "COM8")
switch.connect()

while 1:
	switch.button_click(100, ["du", "ls", "zl", "b", "x", "+"])
```