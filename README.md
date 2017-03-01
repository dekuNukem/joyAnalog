# A hub for my Nintendo Switch related projects

I'm going to put all my resources and discoveries related to Nintendo Switch here, which will probably be updated frequently in the coming days after the launch.

## NintenDAC dev board for Nintendo Switch modification

NintenDAC is a STM32 development board with up to 10 high-speed 12-bit DAC channels. I intend to use it for automating Joycon inputs, and maybe it would be suitable for TAS as well. 

The board has 2 versions. The smaller NintenDAC mini (left) is intended to be used on a Joycon, while the bigger NintenDAC (right) has more GPIOs and a dedicated high-speed DAC chip, and is suitable for modifying the pro controller or the console itself.

![Alt text](http://i.imgur.com/zYkvhDJ.jpg)

Both present themselves to PC as a USB serial port, so no special drivers are needed. Simply connect the button and joystick test points to the headers to allow the joycon be controlled from a PC.

## Board resources, communication protocol and Python library

For NintenDAC mini: [click here](./NintenDAC_mini)

For NintenDAC: [click here (still under construction)](./NintenDAC)

## Assembly tutorials

Coming soon after I got my Switch

## Twitch Plays Nintendo Switch

I dug up and reused a portion of my old code for TwitchPlaysPokemonX, [see here](./TwitchPlaysNintendoSwitch).

