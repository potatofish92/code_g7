import pandas as pd
import numpy as np 
import nidaqmx


from nidaqmx.constants import TerminalConfiguration

# create NI-DAQmx task
with nidaqmx.Task() as task:
    # 
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0",  # 
                                         terminal_config=TerminalConfiguration.DEFAULT,
                                         min_val=-10.0,  # 
                                         max_val=10.0)   # 
    
    # 
    voltage = task.read()
    print(f"voltage get from ai0 :{voltage:.3f} V")


