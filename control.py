
#%%
import time
from pynput.mouse import Controller
from pynput.keyboard import Listener, Key
from dataclasses import dataclass
import threading
# from pynput.keyboard import Listener, Key


#%%
# Create a mouse controller object
mouse = Controller()

#%%
#finish params package
@dataclass
class MouseControlParams:
    mode: int = 0
    grind: bool = False
    # blink_hori_verti: int = 0
    power: bool = False
    def __post_init__(self):
        self.int2str = {
            0: 'horizontal',
            1: 'vertical',
            2: 'left',
            3: 'right',
            4: 'up',
            5: 'down',
        }

    def get_mode_string_value(self):
        return self.int2str.get(self.mode, 'unknown')
    
    
@dataclass
class trigger_signals:
    #change mode
    left_blink: int = 0
    #click
    right_blink: int = 0
    #turn on/off
    grind: int = 0
    #move upward
    up_signal: int = 0
    #move downward
    down_signal: int = 0
    #move leftward
    left_signal: int = 0
    #move rightward
    right_signal: int = 0
#%%
##TODO : Add power switch function
class MouseController:
    def __init__(self, params: MouseControlParams, signals: trigger_signals,move_step: float = 2.0):
        self.params = params
        self.move_step = move_step
        self.current_x, self.current_y = mouse.position
        self.current_mode: str = params.get_mode_string_value()
        self.signals = signals
        # self.currrent_mode: str = params.get_mode_string_value(self.params.mode)
    def move_mouse(self, tmp_mode: int): #maybe include every params in this function
        tmp_mode = self.current_mode
        if not self.params.power : 
            print("Power is currently off,")
            print("Please turn on the power to continue")
            return
        
        elif self.current_mode == 'left':
            self.current_x -= self.move_step
            
        elif self.current_mode == 'right':
            self.current_x += self.move_step
        
        elif self.current_mode == 'up':
            self.current_y -= self.move_step
        
        elif self.current_mode == 'down':
            self.current_y += self.move_step
            
        # Move the mouse to the new position
        mouse.position = (self.current_x, self.current_y)
        # Print the current position
        print(f'Mouse moved to {mouse.position}')

    def power_switch(self):
        if self.params.grind:
            self.params.power = not self.params.power
            print(f'Power is now {self.params.power}')
            
    #TODO: add the function of controlling the mouse params
    def mouse_mode_control(self):
        if self.signals.left_blink == 10:
            if self.params.mode == 0:
                self.params.mode = 1
            if self.params.mode == 1:
                self.params.mode = 0
            self.currrent_mode = self.params.get_mode_string_value()
            print(f'Mouse mode is now {self.currrent_mode}')
        else :
            if self.params.power:
                if self.params.mode == 0:
                    if self.signals.left_signal == 10:
                        self.params.mode = 2
                    if self.signals.right_signal == 10:
                        self.params.mode = 3
                elif self.params.mode == 1:
                    if self.signals.up_signal == 10:
                        self.params.mode = 4
                    if self.signals.down_signal == 10:
                        self.params.mode = 5
                self.currrent_mode = self.params.get_mode_string_value()
                    
    #function to control mouse movement mode
'''
every signal is : 
0v when turned off, 
10v when turned on
'''
# Function to handle signal interrupt events
# def eye_signal_detecter(self) -> trigger_signals:
#     with Listener(on_press=lambda key: self.on_press(key, self.signals, self), on_release=self.on_release) as listener:
#         listener.join()



#function to control the blink mode


#%%
# Example usage
# @staticmethod
def on_press(key) :
    try:
        if key.char == 'a':
            controller.signals.left_signal = 10
            # return self.psuedo_signals
        elif key.char == 'd':
            controller.signals.right_signal = 10
            # return self.psuedo_signals
        elif key.char == 'w':
            controller.signals.up_signal = 10
            # return self.psuedo_signals
        elif key.char == 's':
            controller.signals.down_signal = 10
            # return self.psuedo_signals
        elif key.char == 'p':
            controller.signals.grind = 10
            # return self.psuedo_signals
        elif key.char == 'o':
            controller.signals.left_blink = 10
            # return self.psuedo_signals
        
    except AttributeError:
        pass
    
# @staticmethod
def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

params = MouseControlParams()
signals = trigger_signals()
controller = MouseController(params=params, signals=signals, move_step=10.0)

with Listener(on_press=lambda key: on_press(key, signals, controller), on_release=on_release) as listener:
    listener.join()



##TODO:start monitoring the datas    
#%%
# # Start the grind monitoring in a separate thread
# grind_thread = threading.Thread(target=controller.monitor_grind)
# grind_thread.daemon = True
# grind_thread.start()

# # Start the blink monitoring in a separate thread
# blink_thread = threading.Thread(target=controller.monitor_blink)
# blink_thread.daemon = True
# blink_thread.start()

# # Start the grind monitoring in a separate thread
# movement_thread = threading.Thread(target=controller.monitor_movement)
# movement_thread.daemon = True
# movement_thread.start()

#%%
# Simulate continuous data input with power control
# def continuous_data_input(controller):
#     directions = ['left', 'right', 'up', 'down']
#     index = 0
#     while True:
#         direction = directions[index % len(directions)]
#         controller.move_mouse(direction)
#         index += 1
#         time.sleep(0.5)  # Simulate delay between data inputs

# try:
#     # Start the continuous data input
#     continuous_data_input(controller)
# except KeyboardInterrupt:
#     print("Script terminated by user")