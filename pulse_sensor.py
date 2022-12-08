import serial
from sys import platform
import numpy as np
import time
from data_saving import DataSaver

''''' IMPORTS PULSE DATA FROM ARDUINO '''''


class PulseSensor:
    def __init__(self, filepath):
        # keep track of all values (valid and invalid ones)
        self.data_log = np.empty(shape=[0, 3])
        self.data_saver = DataSaver(filepath, ["timestamp", "BPM", "pulse_data"])

        # check current operating system and connect to arduino serial
        if platform == "darwin":  # Mac
            self.arduino = serial.Serial('/dev/cu.usbmodem14101', 9600, timeout=1)
            # self.arduino = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
        else:  # platform == "linux":  # maybe raspi??
            self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            print ("what is this system????????????????")

        self.arduino.flush()

        # wait for connection
        time.sleep(1)

    def get_pulse_data(self):
        if self.arduino.in_waiting > 0:
            # read from Arduino serial output and convert
            # byte string to string array [bpm, pulse_signal]
            try:
                data = self.arduino.readline().decode('utf-8').rstrip().split(',')

                # try to convert data array entries: bpm and pulse data to int
                bpm = int(data[0])
                pulse_signal = int(data[1])
                timestamp = time.time()
                # print([bpm, pulse_signal])

                # add new data to log
                self.data_log = np.append(self.data_log, [[timestamp, bpm, pulse_signal]], axis=0)

                return [timestamp, bpm, pulse_signal]
            except Exception as e:
                print("error while converting")
                # print("BPM: " + str(bpm) + ", PULSE SIGNAL: " + str(pulse_signal))
                print(e)

        return [0, 0, 0]

    def close_connection(self):
        # close serial connection
        self.arduino.close()
        self.data_saver.save_datalog_array(self.data_log)

