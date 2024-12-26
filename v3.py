import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import time
import matplotlib.pyplot as plt

DEVICE_NAME = "Dev2/ai0"
SAMPLE_RATE = 1000
BUFFER_SIZE = 100

try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(
            DEVICE_NAME,
            terminal_config=TerminalConfiguration.DEFAULT,
            min_val=-10.0,
            max_val=10.0,
        )
        task.timing.cfg_samp_clk_timing(
            rate=SAMPLE_RATE, 
            sample_mode=AcquisitionType.CONTINUOUS
        )

        print("Starting real-time acquisition... Press Ctrl+C to stop.")

        while True:
            data = task.read(number_of_samples_per_channel=BUFFER_SIZE)
            print(f"Read {len(data)} samples: {data}")
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Acquisition stopped by user.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Task resources released.")
