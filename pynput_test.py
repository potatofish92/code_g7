import time
import math
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key
from dataclasses import dataclass

# Create a mouse controller object
mouse = Controller()

@dataclass
class mouse_control_params:
    power: bool = False
    mode: str = 'horizontal'
    grind: bool = False
    blink_hori_verti: int = 0
    @classmethod
    def power_switch(cls):
        if cls.grind:
            cls.power = not cls.power


class MouseMovement:
    move_step: float
    duration: float
    current_x: int
    current_y: int
    
    def __init__(
        self, 
        duration: int,
        current_x: int,
        current_y: int,
        move_step: float = 1.0, 
    ):
        self.move_step = move_step
        self.duration = duration
        self.current_x, self.current_y = mouse.position
    
    # Function to move the mouse in a circular pattern
    def move_mouse_horizontal(self):
        x, y = mouse.position
        start_time = time.time()
        while time.time() - start_time < self.duration:    
            # Calculate the new position
            # Function to detect key press
            def on_press(key):
                if key == Key.esc:
                    # Stop listener
                    return False
                if key == Key.right:
                    # Stop listener
                    return
            # Start the keyboard listener
            listener = Listener(on_press=on_press)
            listener.start()
            x = x + self.move_step * 0.1 
            # y = y
            # Move the mouse to the new position
            mouse.position = (x, y)
            # Print the current position
            print(f'Mouse moved to {mouse.position}')
            # Small delay to make the movement smoother
            time.sleep(0.01)

try:
        movement = MouseMovement(100, 500, 500)
        movement.move_mouse_horizontal()
        # Move the mouse in a circle with radius 100 around the center (500, 500) for 10 seconds
        # move_mouse_horizontal(100, 10)

except KeyboardInterrupt:
    print("Script terminated by user")