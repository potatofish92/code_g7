import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
from dataclasses import dataclass


#map the data into the corresponding signal
trigger_signals = {
    'Dev2/ai0': 'grind',
    'Dev2/ai1': 'left_blink',
    'Dev2/ai2': 'right_blink',
    'Dev2/ai3': 'left_signal',
    'Dev2/ai4': 'right_signal'
}

# 設置數據讀取的參數
sampling_rate = 1000 
channels = ['Dev2/ai0', 'Dev2/ai1', 'Dev2/ai2', 'Dev2/ai3', 'Dev2/ai4']  # 要讀取的通道
#             grind,   left_blink, right_blink, left_signal, right_signal

BUFFER_SIZE = 1
@dataclass
class Triggers:
    def __init__(self):
        self.left_blink: int = 0
        self.right_blink: int = 0
        self.grind: int = 0
        # self.up_signal: int = 0
        # self.down_signal: int = 0
        self.left_signal: int = 0
        self.right_signal: int = 0

    # define the function to output the datas respectively
    def collect_data(self):
        return {
            "left_blink": self.left_blink,
            "right_blink": self.right_blink,
            "grind": self.grind,
            # "up_signal": self.up_signal,
            # "down_signal": self.down_signal,
            "left_signal": self.left_signal,
            "right_signal": self.right_signal,
        }

    def find_variable(self, variable_name):
        return getattr(self, variable_name, None)


# 創建任務
# task = nidaqmx.Task()
signals = Triggers()

try:
    with nidaqmx.Task() as task:
# 添加通道到任務中
        for channel in channels:
            task.ai_channels.add_ai_voltage_chan(
                channel,
                terminal_config=TerminalConfiguration.DEFAULT,
                min_val=-10.0,
                max_val=10.0,
            )
        # 設置採集參數
        task.timing.cfg_samp_clk_timing(
            sampling_rate, 
            sample_mode=AcquisitionType.CONTINUOUS
            )
        while True:
            data1 = task.read(number_of_samples_per_channel=BUFFER_SIZE)
            
            data = {channel: [] for channel in channels}
            
            for i, channel in enumerate(channels):
                data[channel] = data1[i]
            
            signals.grind = data['Dev2/ai0']
            
            # Update the signals based on the channel data
            for channel, signal_name in trigger_signals.items():
                setattr(signals, signal_name, channel)

            # print(signals.collect_data())
            print(data)

            # 初始化數據存儲
            #store the data in a dictionary called data with each channel's name as the key to access the data

            
except KeyboardInterrupt:
    print("Acquisition stopped by user.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Task resources released.")

            


# 設置繪圖
# fig, axs = plt.subplots(len(channels), 1, figsize=(10, 6))
# lines = {channel: ax.plot([], [], label=channel)[0] for channel, ax in zip(channels, axs)}
# for ax in axs:
#     ax.set_xlim(0, 100)  # 初始 x 軸範圍
#     ax.set_ylim(-10, 10)  # y 軸範圍
#     ax.legend() # 顯示圖例

# # 更新繪圖的函數
# def update():
#     samples = task.read(number_of_samples_per_channel=sampling_rate)
#     for i, channel in enumerate(channels):
#         data[channel].extend(samples[i])
#         lines[channel].set_data(range(len(data[channel])), data[channel])
    
#     # 動態調整 x 軸範圍
#     for ax in axs:
#         ax.set_xlim(max(0, len(data[channels[0]]) - 100), len(data[channels[0]]))
    
#     return lines.values()

# # 創建動畫
# ani = FuncAnimation(fig, update, interval=100)

# # 開始繪圖
# plt.show()

