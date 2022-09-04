import os, signal
from pynput import keyboard
import numpy


def on_press(key):
    try:
        pass
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key, ):
    if key == keyboard.Key.esc:
        print('\033[36m Process {} is over\033[0m'.format(os.getpid()))
        os.kill(os.getpid(), signal.SIGTERM)
        return False
