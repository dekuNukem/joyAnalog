joyAnalog is a custom STM32 board with 12 analog switches and 2 12-bit DAC channels. Its main purpose is for automating Nintendo Switch Joycon inputs, and maybe it would be suitable for TAS as well. 

This project was previously named NintenDAC, and had two versions. I started working on them before Nintendo Switch came out, and assumed that the button would be in one-side-pulled-up-other-side-to-ground configuration as it has always been. However as it turned out Joycon and Pro controller uses keypad scanning for reading buttons, rendering my original design useless. 

So I started a new design featuring 2 SPI analog switches that connects the buttons to the common column input, therefore activating the buttons. 2 built-in DAC will be able to take over the joystick input.

joyAnalog presents itself to PC as a virtual USB serial port, so no special drivers are needed. Simply connect the button and joystick test points to the headers to allow the Joycon be controlled from a PC.

## Board resources, communication protocol and Python library

Updating....

## Twitch Plays Nintendo Switch

I dug up and reused a portion of my old code for TwitchPlaysPokemonX, [see here](./TwitchPlaysNintendoSwitch).

