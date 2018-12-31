Overview:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The chronoSync script was made to: 
Automate labeling of EEG data syncronized in time with controller input for machine learning.
This autonomy is needed because we are attempting to find out if patterns exist in EEG data corresponding to the motor actions of keypresses.
Below is a breakdown of each section of the code, followed by a note on its implementation.


Specifics of the code:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The motor cortex of the brain is on the outer most layer of the pre-frontal cortex, giving a good chance that if unique patterns of brainwave 
activity exist, then EEG data has the best chance of picking up unique patterns for forward, backward, left or right (W,A,S,D)

Problem: 
Given a keylogger with milisecond accuracy (see readme for logger.py in this folder), and EEG data with milisecond accuracy,
how do you format EEG data labeled with the keylogger. Additionally, what window of samples before the keypress do you use for each label?

Solution:
chronoSync allows the user to specify what keys the user wishes to track on a keyboard, and how many samples of EEG 
data before the keypress to capture and attempt to correlate with machine learning to the specific keypress. The logic is as follows.
In the first phase of the algorith, a logfile of control data is parsed looking for the specific keys the user specifies in the beginning of the script.
1) The script opens a logfile of control data and parses it for the keys the user specifies in the beginning of their script and the timestamp it was pressed.
    The List of dictionaries is formatted: [HH:MM:SS.XYZ : 'key', HH:MM:SS.XYZ : 'key, ...]

2) The script then parses the EEG file building up a window of X samples with N electrodes per sample (8 in our case) and a timestamp of the sample
    If the timestamp of the X+1 sample is roughly equal - omitting the last decimal place because keystrokes are slow compared to EEG - 
    The entire list of X samples of data is given one final element (the key that corresponds with that timestamp) then saved in another list.
    By the end of this step there is a list of X samples of EEG data with the label as the last element.

3) The final step is to take the list produced above, create a uniquely named logfile, and iterate through the list of sample windows and keys.
    This step extracts only the relevant EEG data, then fills the logfile with chronologically syncronized EEG data with a keypress label.
    By the end of the script, a CSV file is produced with entries that look like this:
    electrode1, electrode2...., keypressA
    electrode1, electrode2...., keypressB
    With each line's CSV data in the order it was sampled in.

How to implement with machine learning:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The final format of the logfile is in the standard format for one hot encoding. 
We are currently in the process of training a network on this data to predict the control input given ONLY EEG data and a window size.
There is now way of knowing presently HOW MANY samples preceeding a keypress will yeild the best accuracy of the network's prediction.
500 samples (0.5 seconds at 1kHz sampling) may contain several spikes of data indicative of a certain keypress, or it may contain too much data.
If the sampling window is too large the machine learning may lose the patterns contained in the data, whereas a small window may clip patterns.

While the initial selection of window size will be hand picked, it may be beneficial to write a meta-training algorithm that does the following.
Trains a network on a large data set of EEG and control input choosing X samples of data to train the network on.
Tests the performance of the network on EEG data it has not been trained on whose control inputs are known.
Saves the performance of the network, then tests X(+/-)delta samples and evaluates the performance of those networks.
If they perform better, the algorithm then tests along that direction until it finds an optimal number X of samples. 

