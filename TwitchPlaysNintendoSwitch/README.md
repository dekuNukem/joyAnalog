# Twitch Plays Nintendo Switch

This is actually a simplified version of the code used during TwitchPlaysPokemonX back in 2014. To keep it simple I used  tkinter for the command scroller. 

To use it:

* Connect the two correctly configured NintenDAC mini board to the PC

* Open up `launch.py` and configure the username, oauth, chat channel and serial port name.

* Open up `banned_user.txt` and `disabled_cmd.txt` and fill them in as you wish. These can be updated while main script is running too.

* Run `python3 launch.py`

This script was tested under windows 10, it should work in macOS and linux too.