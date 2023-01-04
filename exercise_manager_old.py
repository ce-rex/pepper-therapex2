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
        # prepare file for saving data
        self.session_num = 1
        self.experiment_timestamp = time.strftime("%Y-%m-%d_%H%M", time.localtime())
        self.filename = "data_log/" + self.experiment_timestamp + "-session" + str(self.session_num) + ".csv"
        self.headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
        self.data_saver = DataSaver(self.filename, self.headers)

        if arduino:
            # connect to Arduino for pulse data from sensor
            self.sensor = PulseSensor()
        else:
            self.sensor = ArtificialPulseSensor()

        self.last_bpm = 0
        self.last20_bpm = np.arange(-20, 0)
        self.last20_bpm_variance = 100  # some number greater than 1

        self.resting_bpm = -1
        self.lower_bound_bpm = 0
        self.upper_bound_bpm = 0

        self.is_calibrating = False
        self.is_requesting_exercise_intensity = False
        self.exercise_intensity = np.nan
        # self.current_intensity = np.nan

    def update_data(self):
        # get new sensor data
        timestamp, bpm, pulse_signal = self.sensor.get_pulse_data()

        if (bpm != 0) or (pulse_signal != 0):
            # print("BPM: " + str(bpm) + "  ---  pulse signal: " + str(pulse_signal))

            if self.is_calibrating and self.last_bpm != bpm:
                self.calibrate(bpm)

            if self.is_requesting_exercise_intensity:
                current_intensity = self.exercise_intensity
                self.exercise_intensity = np.nan
            else:
                current_intensity = np.nan

            # keep track of time - BPM - pulse data  - resting BPM - exercise intensity
            self.data_saver.save_data([timestamp, bpm, pulse_signal, self.resting_bpm, current_intensity])

            self.last_bpm = bpm

            return [bpm, pulse_signal, self.resting_bpm, current_intensity]

    def start_calibration(self):
        # calc variance until the BPM is stable (variance < 1)
        print("CALIBRATING...")
        self.is_calibrating = True

    def calibrate(self, bpm):
        self.last20_bpm = np.append(self.last20_bpm[1:], [bpm])
        self.last20_bpm_variance = self.last20_bpm.var()

        if self.last20_bpm_variance < 10:
            print("EAR PIECE IS CALIBRATED!")

            # calc resting BPM
            self.resting_bpm = self.last20_bpm.mean()
            print("RESTING BPM: " + str(self.resting_bpm))

            # calc BPM boundaries
            self.lower_bound_bpm = self.resting_bpm * 1.2
            self.upper_bound_bpm = self.resting_bpm * 1.3
            print ("BPM boundaries: " + str(self.lower_bound_bpm) + " --- " + str(self.upper_bound_bpm))

    def get_exercise_intensity(self):
        # evaluate if intensity should stay the same, go up or down
        if self.last_bpm < self.lower_bound_bpm:
            current_intensity = 1
            print("BPM TOO LOW, faster exercise!")
        elif self.last_bpm > self.upper_bound_bpm:
            current_intensity = -1
            print("BPM TOO HIGH, slower exercise!")
        else:
            current_intensity = 0
            print("BPM PERFECT, keep doing what you are doing!")

        self.exercise_intensity = current_intensity
        self.is_requesting_exercise_intensity = True

        return current_intensity

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

        # reset data
        self.last_bpm = 0
        self.last20_bpm = np.arange(-20, 0)
        self.last20_bpm_variance = 100  # some number greater than 1

        self.resting_bpm = -1
        self.lower_bound_bpm = 0
        self.upper_bound_bpm = 0

    def new_data_saver(self):
        print("starting session no. " + str(self.session_num))
        self.filename = "data_log/" + self.experiment_timestamp + "-session" + str(self.session_num) + ".csv"
        self.data_saver = DataSaver(self.filename, self.headers)

    def save_session_data(self):
        print("saving session data!")
        create_plot_from_path(csv_path=self.filename, save_plot=True)

