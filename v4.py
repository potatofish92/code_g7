import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
from dataclasses import dataclass

# 設置數據讀取的參數
SAMPLING_RATE = 60  # 每秒更新次數
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


def main():
    signals = Triggers()

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
                signals.grind = 1 if data["Dev2/ai0"][-1] >= 5 else 0
                signals.left_signal = 1 if data["Dev2/ai3"][-1] >= 5 else 0
                signals.right_signal = 1 if data["Dev2/ai4"][-1] >= 5 else 0
                signals.left_blink = (
                    1 if data["Dev2/ai1"][-1] >= 5 and data["Dev2/ai3"][-1] < 5 else 0
                )
                signals.right_blink = (
                    1 if data["Dev2/ai2"][-1] >= 5 and data["Dev2/ai4"][-1] < 5 else 0
                )

                print(data)
                print(signals.collect_data())

    except KeyboardInterrupt:
        print("Acquisition stopped by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Task resources released.")


if __name__ == "__main__":
    main()
