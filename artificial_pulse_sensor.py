import pandas as pd
from sys import platform
import numpy as np
import time
from data_saving import DataSaver

''''' IMPORTS PULSE DATA FROM ARDUINO '''''


class ArtificialPulseSensor:
    def __init__(self):
        self.test_data = [[63, 435], [61, 378]]
        self.counter = 0

        self.data_log = np.empty(shape=[0, 3])
        # self.data_saver = DataSaver(filepath, ["timestamp", "BPM", "pulse_data"])

    def get_pulse_data(self):
        bpm, pulse_signal = self.test_data[self.counter]
        timestamp = time.time()

        data = [timestamp, bpm, pulse_signal]
        self.data_log = np.append(self.data_log, [[timestamp, bpm, pulse_signal]], axis=0)
        self.counter = (self.counter + 1) % 2

        return data

    def close_connection(self):
        # close serial connection
        print("if I'd be an arduino I would close the connection now")
        # self.data_saver.save_datalog_array(self.data_log)
