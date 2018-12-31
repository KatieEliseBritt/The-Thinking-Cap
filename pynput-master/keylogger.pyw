
#Script logs key presses when activated for later syncing important keys with EEG data
#written 11/29/18 by Katie Britt 
from pynput.keyboard import Key, Listener
import logging

log_dir = ""

logging.basicConfig(filename=(log_dir + "logs.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s:')

def on_press(key): 
    logging.info(str(key))

with Listener(on_press=on_press) as listener:
    listener.join()