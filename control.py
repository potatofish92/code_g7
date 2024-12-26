# %%
import time
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key
from dataclasses import dataclass
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import matplotlib.pyplot as plt


# %%
# Create a mouse controller object
mouse = Controller()


# %%
# finish params package
@dataclass
class Params:
    mode: int = 0
    power: bool = False
    movestep: int = 5
    mode2str = {
        0: "horizontal",
        1: "vertical",
        2: "hori-left",
        3: "hori-right",
        4: "verti-up",
        5: "verti-down",
    }
    power2str = {
        0: "off",
        1: "on",
    }

    def inform(self):
        mode_str: str = self.mode2str.get(self.mode, "unknown")
        power_str: str = self.power2str.get(self.power, "unknown")
        return {"mode": mode_str, "power": power_str}


@dataclass
class Triggers:
    left_blink: int = 0
    right_blink: int = 0
    grind: int = 0
    left_signal: int = 0
    right_signal: int = 0

    def collect_data(self):
        return {
            "left_blink": self.left_blink,
            "right_blink": self.right_blink,
            "grind": self.grind,
            "left_signal": self.left_signal,
            "right_signal": self.right_signal,
        }

    def find_variable(self, variable_name):
        return getattr(self, variable_name, None)


class Position:
    def __init__(self, x=959, y=539):
        self.x = x
        self.y = y

    def update(self, dx, dy):
        self.x += dx
        self.y += dy


# %%
##TODO : Add power switch function
class MouseController:
    def __init__(self, signals: Triggers, move_step: float = 2.0):
        self.params = Params()
        self.signals = signals
        self.position = Position(*mouse.position)
        self.move_step = move_step
        self.current_power = "on" if self.params.power else "off"
        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
        print(f"Initial status of MouseController: {self.current_mode}")
        print(f"Initial power status of MouseController: {self.current_power}")

    # movement corresponding to the mode
    def update_position(self):
        if not self.params.power:
            print("Power is currently off,")
            print("Please turn on the power to continue")
            return

        if self.params.mode == 2:  # left
            while self.params.power:
                self.position.update(-self.move_step, 0)
                time.sleep(0.1)
                
        elif self.params.mode == 3:  # right
            while self.params.power:
                self.position.update(self.move_step, 0)
                time.sleep(0.1)
        elif self.params.mode == 4:  # up
            while self.params.power:
                self.position.update(0, -self.move_step)
                time.sleep(0.1)
        elif self.params.mode == 5:  # down
            while self.params.power:
                self.position.update(0, self.move_step)
                time.sleep(0.1)

        # Move the mouse to the new position
        self.mouse.position = (self.position.x, self.position.y)
        # Print the current position
        print(f"Mouse moved to {self.mouse.position}")


    def power_switch(self, signals: Triggers):
        if signals.grind:
            self.params.power = not self.params.power
        self.current_power: str = "on" if self.params.power else "off"
        print(f"Power is now {self.current_power}")

    # TODO: add the function of controlling the mouse params
    def mouse_mode_control(self, signals: Triggers):
        if self.params.power:
            # change to left
            if self.params.mode == 0 and signals.left_signal :
                self.params.mode = 2
            # change to right
            elif self.params.mode == 0 and signals.right_signal :
                self.params.mode = 3
            # change to up
            elif self.params.mode == 1 and signals.right_signal :
                self.params.mode = 4
            # change to down
            elif self.params.mode == 1 and signals.left_signal :
                self.params.mode = 5
           
            # error message
            if signals.left_blink:
                print("Please turn off the power to continue changing the mode")
                self.current_power: str = "on" if self.params.power else "off"
                print(f"MouseController is now {self.current_power}")
            
            #broadcast the mode
            self.current_mode = self.params.get_mode_string_value(self)
            print(f"MouseController is now in {self.current_mode} mode")

        else:
            if self.params.mode == 2 or self.params.mode == 3:
                    self.params.mode = 0
            elif self.params.mode == 4 or self.params.mode == 5:
                self.params.mode = 1       
            
            if self.signals.left_blink:
                self.params.mode = 1 if self.params.mode == 0 else 0
            

            if self.signals.left_signal or self.signals.right_signal:
                print("Please turn on the power to do the movement")
                self.current_power: str = "on" if self.params.power else "off"
                print(f"MouseController is now {self.current_power}")

            self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
            print(f"MouseController is now in {self.current_mode} mode")

    # function to control mouse movement mode


def main():
    signals = Triggers()
    controller = MouseController(signals=signals, move_step=10.0)

    def on_press(key):
        try:
            if key.char == 'a':
                controller.params.mode = 2  # left
            elif key.char == 'd':
                controller.params.mode = 3  # right
            elif key.char == 'w':
                controller.params.mode = 4  # up
            elif key.char == 's':
                controller.params.mode = 5  # down
        except AttributeError:
            pass

    def on_release(key):
        if key == Key.esc:
            controller.params.power = False
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        while controller.params.power:
            controller.update_position()
            controller.mouse_mode_control()
            time.sleep(0.1)
        listener.join()

if __name__ == "__main__":
    main()