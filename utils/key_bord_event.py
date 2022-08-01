import os,signal
from functools import partial
from pynput import keyboard
import numpy
def on_press(key):
    try:
        pass
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key,):
    if key ==keyboard.Key.esc:
        print('Program is over')
        os.kill(os.getpid(), signal.SIGTERM)
        return False