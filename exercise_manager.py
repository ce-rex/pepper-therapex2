from pulse_sensor import PulseSensor
from artificial_pulse_sensor import ArtificialPulseSensor
from data_plotter import *
# from constants import *
import numpy as np
import time
import random
from data_saving import DataSaver


class ExerciseManager:
    def __init__(self, arduino):
        # initialize data saver
        self.headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
        self.session_num = 0
        self.experiment_timestamp = ""
        self.filename = ""
        self.data_saver = None

        if arduino:
            # connect to Arduino for pulse data from sensor
            self.sensor = PulseSensor()
        else:
            self.sensor = ArtificialPulseSensor()

        self.resting_bpm = -1
        self.exercise_intensity = np.nan

    def update_data(self):
        # get new sensor data
        timestamp, bpm, pulse_signal = self.sensor.get_pulse_data()

        if (bpm != 0) or (pulse_signal != 0):
            # print("BPM: " + str(bpm) + "  ---  pulse signal: " + str(pulse_signal))

            # keep track of time - BPM - pulse data  - resting BPM - exercise intensity
            self.data_saver.save_data([timestamp, bpm, pulse_signal, self.resting_bpm, self.exercise_intensity])

            if self.exercise_intensity != np.nan:
                self.exercise_intensity = np.nan

            return [bpm, pulse_signal]

    def stop_everything(self):
        # close connection to arduino
        self.sensor.close_connection()

    def start_new_session(self):
        self.session_num += 1
        self.new_data_saver()

    def start_new_experiment_cycle(self):
        print("new experiment cycle!")
        # data saving
        self.session_num = 1
        self.experiment_timestamp = time.strftime("%Y-%m-%d_%H%M", time.localtime())
        self.new_data_saver()

    def new_data_saver(self):
        print("starting session no. " + str(self.session_num))
        self.filename = "data_log/" + self.experiment_timestamp + "-session" + str(self.session_num) + ".csv"
        self.data_saver = DataSaver(self.filename, self.headers)

    def save_session_data(self):
        print("saving session data!")
        create_plot_from_path(csv_path=self.filename, save_plot=True)

