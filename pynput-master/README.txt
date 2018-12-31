The python script, keylogger.pyw, records key presses
in a log file for the purpose of consolidating our
EEG data into useful matrices for our supervised 
learning network. It works by doing the following:

	1. Call keylogger.pyw from the terminal. The
	   "pyw" extension allows it to run in the
	   background.
	2. The script logs keypresses in a json format
	   while active. This will be used to record
	   directional keys pressed and the timestamps
	   of each key pressed while someone is playing 
	   a videogame.
	3. Use "CTRL:SHIFT:ESC" to terminate the program
	   (or end the python process). The output file, 
	   "log.txt" should be available in the folder.

The other folders and documents in this folder are what
enable the libraries used in the keylogger.pyw script to
work and were found on github: 
	https://github.com/moses-palmer/pynput
	