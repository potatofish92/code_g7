import time
from pynput.mouse import Controller
from time import sleep
from pynput.keyboard import Listener, Key
from dataclasses import dataclass
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration

# import matplotlib.pyplot as plt

mouse = Controller()


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
    left_blink: bool = 0
    right_blink: bool = 0
    grind: bool = 0
    left_signal: bool = 0
    right_signal: bool = 0

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
    def __init__(self, x=mouse.position[0], y=mouse.position[1]):
        self.x = x
        self.y = y

    def update(self, dx, dy):
        self.x += dx
        self.y += dy


class MouseController:
    def __init__(self, signals: Triggers, move_step: int = 2):
        self.params = Params()
        self.signals = signals
        self.position = Position(*mouse.position)
        self.move_step = move_step
        self.current_power = "on" if self.params.power else "off"
        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
        print(f"Initial status of MouseController: {self.current_mode}")
        print(f"Initial power status of MouseController: {self.current_power}")

    def update_signals(self, signals: Triggers):
        self.signals = signals

    # movement corresponding to the mode
    def update_position(self, signals: Triggers):
        if not self.params.power:
            print("Power is currently off,")
            print("Please turn on the power to continue")
        else:
            clock=0
            if self.params.mode == 2:  # left
                self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                self.current_power = "off" if not self.params.power else "on"
                print(f"MouseController is now in {self.current_mode} mode")
                print(f"Power is now {self.current_power}")
                while self.params.power:
                    self.position.update(-self.move_step, 0)
                    mouse.position = (self.position.x, self.position.y)
                    # Move the mouse to the new position
                    mouse.position = (self.position.x, self.position.y)
                    # Print the current position
                    print(f"Mouse moved to {mouse.position}")
                    clock+=1
                    if clock==20:
                        self.params.mode = 0
                        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                        self.params.power = False
                        self.current_power = "off"
                        print(f"MouseController is now in {self.current_mode} mode")
                        print(f"Power is now {self.current_power}")
                        time.sleep(0.5)
                        break
                    time.sleep(0.1)
            elif self.params.mode == 3:  # right
                self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                self.current_power = "off" if not self.params.power else "on"
                print(f"MouseController is now in {self.current_mode} mode")
                print(f"Power is now {self.current_power}")
                while self.params.power:
                    self.position.update(self.move_step, 0)
                    mouse.position = (self.position.x, self.position.y)
                    # Move the mouse to the new position
                    mouse.position = (self.position.x, self.position.y)
                    # Print the current position
                    print(f"Mouse moved to {mouse.position}")
                    clock+=1
                    if clock==20:
                        print("grind signal detected")
                        self.params.mode = 0
                        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                        self.params.power = False
                        self.current_power = "off"
                        print(f"MouseController is now in {self.current_mode} mode")
                        print(f"Power is now {self.current_power}")
                        time.sleep(0.5)
                        break
                    time.sleep(0.1)
            elif self.params.mode == 4:  # up
                self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                self.current_power = "off" if not self.params.power else "on"
                print(f"MouseController is now in {self.current_mode} mode")
                print(f"Power is now {self.current_power}")
                while self.params.power:
                    self.position.update(0, -self.move_step)
                    mouse.position = (self.position.x, self.position.y)
                    # Move the mouse to the new position
                    mouse.position = (self.position.x, self.position.y)
                    # Print the current position
                    print(f"Mouse moved to {mouse.position}")
                    clock+=1
                    if clock==20:
                        print("grind signal detected")
                        self.params.mode = 1
                        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                        self.params.power = False
                        self.current_power = "off"
                        print(f"MouseController is now in {self.current_mode} mode")
                        print(f"Power is now {self.current_power}")
                        time.sleep(0.5)
                        break
                    time.sleep(0.1)
            elif self.params.mode == 5:  # down
                self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                self.current_power = "off" if not self.params.power else "on"
                print(f"MouseController is now in {self.current_mode} mode")
                print(f"Power is now {self.current_power}")
                while self.params.power:
                    self.position.update(0, self.move_step)
                    mouse.position = (self.position.x, self.position.y)
                    # Move the mouse to the new position
                    mouse.position = (self.position.x, self.position.y)
                    # Print the current position
                    print(f"Mouse moved to {mouse.position}")
                    print(f'params: {self.params}')
                    clock+=1
                    if clock==20:
                        print("grind signal detected")
                        self.params.mode = 1
                        self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
                        self.params.power = False
                        self.current_power = "off"
                        print(f"MouseController is now in {self.current_mode} mode")
                        print(f"Power is now {self.current_power}")
                        time.sleep(0.5)
                        break
                    time.sleep(0.1)
            elif self.params.mode == 0 or self.params.mode == 1:
                print("Please change to the corresponding mode to move the mouse")
            

    def power_switch(self):
        if self.signals.grind:
            self.params.power = not self.params.power
        self.current_power: str = "on" if self.params.power else "off"
        print(f"Power is now {self.current_power}")
        print(f'params: {self.params}')

    def mouse_mode_control(self):
        if self.params.power:
            print(f'power is now {self.params.power}')
            print(f'params: {self.params}')
            # change to left
            if self.params.mode == 0 and self.signals.left_signal:
                self.params.mode = 2
            # change to right
            elif self.params.mode == 0 and self.signals.right_signal:
                self.params.mode = 3
            # change to up
            elif self.params.mode == 1 and self.signals.right_signal:
                self.params.mode = 4
            # change to down
            elif self.params.mode == 1 and self.signals.left_signal:
                self.params.mode = 5

            # error message
            if self.signals.left_blink:
                print("Please turn off the power to continue changing the mode")
                self.current_power: str = "on" if self.params.power else "off"
                print(f"MouseController is now {self.current_power}")

            # broadcast the mode
            self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
            print(f"MouseController is now in {self.current_mode} mode")

        else:
            if self.signals.left_blink:
                self.params.mode = 1 if self.params.mode == 0 else 0
                time.sleep(1)
            elif self.params.mode == 2 or self.params.mode == 3:
                self.params.mode = 0
            elif self.params.mode == 4 or self.params.mode == 5:
                self.params.mode = 1

            
            # if self.signals.left_signal or self.signals.right_signal:
            #     print("Please turn on the power to do the movement")
            #     self.current_power: str = "on" if self.params.power else "off"
            #     print(f"MouseController is now {self.current_power}")

            self.current_mode = self.params.mode2str.get(self.params.mode, "unknown")
            print(f"MouseController is now in {self.current_mode} mode")

    # function to control mouse movement mode


# 設置數據讀取的參數
SAMPLING_RATE = 1  # 每秒更新次數
CHANNELS = ["Dev2/ai0", "Dev2/ai1", "Dev2/ai2", "Dev2/ai3", "Dev2/ai4"]  # 要讀取的通道
BUFFER_SIZE = 1

# 將數據映射到對應的信號
TRIGGER_SIGNALS = {
    "Dev2/ai0": "grind",
    "Dev2/ai1": "left_blink",
    "Dev2/ai2": "right_blink",
    "Dev2/ai3": "left_signal",
    "Dev2/ai4": "right_signal",
}


def main():
    signals = Triggers()
    MouseCon = MouseController(signals, move_step=5)

    try:
        with nidaqmx.Task() as task:
            # 添加通道到任務中
            for channel in CHANNELS:
                task.ai_channels.add_ai_voltage_chan(
                    channel,
                    terminal_config=TerminalConfiguration.DEFAULT,
                    min_val=-10.0,
                    max_val=10.0,
                )
            # 設置採集參數
            task.timing.cfg_samp_clk_timing(
                SAMPLING_RATE, sample_mode=AcquisitionType.CONTINUOUS
            )

            while True:
                data1 = task.read(number_of_samples_per_channel=BUFFER_SIZE)
                data = {channel: data1[i] for i, channel in enumerate(CHANNELS)}

                # 更新信號
                for channel, signal_name in TRIGGER_SIGNALS.items():
                    setattr(signals, signal_name, data[channel][0])

                # 更新信號狀態
                data["Dev2/ai1"][-1]=data["Dev2/ai3"][-1]
                data["Dev2/ai2"][-1]=data["Dev2/ai4"][-1]
                signals.grind = 1 if data["Dev2/ai0"][-1] >= 5 else 0
                signals.left_signal = 1 if data["Dev2/ai3"][-1] >= 5 else 0
                signals.right_signal = 1 if data["Dev2/ai4"][-1] >= 5 else 0
                signals.left_blink = (
                    1 if data["Dev2/ai1"][-1] >= 5 else 0
                )
                signals.right_blink = (
                    1 if data["Dev2/ai2"][-1] >= 5 else 0
                )

                print(data)
                print(signals.collect_data())
                MouseCon.update_signals(signals)
                MouseCon.power_switch()
                MouseCon.mouse_mode_control()
                MouseCon.update_position(signals)

    except KeyboardInterrupt:
        print("Acquisition stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Task resources released.")


if __name__ == "__main__":
    main()