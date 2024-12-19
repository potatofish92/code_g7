'''
will need to control the mouse with the keyboard w a s d
and the mouse will move in the direction of the key pressed
and will stop when the key is released
which means it only moves when the key is pressing
'''

import time
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key
from dataclasses import dataclass

# Create a mouse controller object
mouse = Controller()

@dataclass
class MouseControlParams:
    mode: str = 'horizontal'
    grind: bool = False
    blink_hori_verti: int = 0

class MouseController:
    def __init__(self, params: MouseControlParams, move_step: float = 10.0):
        self.params = params
        self.move_step = move_step
        self.current_x, self.current_y = mouse.position

    def move_mouse(self, direction):
        if direction == 'left':
            self.current_x -= self.move_step
        elif direction == 'right':
            self.current_x += self.move_step
        elif direction == 'up':
            self.current_y -= self.move_step
        elif direction == 'down':
            self.current_y += self.move_step
        # Move the mouse to the new position
        mouse.position = (self.current_x, self.current_y)
        # Print the current position
        print(f'Mouse moved to {mouse.position}')

# Function to handle key press events
def on_press(key):
    try:
        if key.char == 'a':
            controller.move_mouse('left')
        elif key.char == 'd':
            controller.move_mouse('right')
        elif key.char == 'w':
            controller.move_mouse('up')
        elif key.char == 's':
            controller.move_mouse('down')
    except AttributeError:
        pass

# Function to handle signal interrupt events
def eye_signal_trigger():
    pass

# Function to handle key release events
def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

# Example usage
params = MouseControlParams(mode='horizontal', grind=False, blink_hori_verti=0)
controller = MouseController(params=params, move_step=10.0)

# Start listening to keyboard events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()