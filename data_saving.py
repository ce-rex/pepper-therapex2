import pandas as pd
import numpy as np
import os


class DataSaver:
    def __init__(self, filename, data_headers):
        # create file and set file format
        self.filename = filename
        self.headers = data_headers
        df = pd.DataFrame(columns=self.headers)

        # create data_saving dir if not exists
        path = "data_log"
        # Check whether the specified path exists or not
        dir_exists = os.path.exists(path)
        if not dir_exists:
            # Create a new directory because it does not exist
            os.makedirs(path)
            print("The new directory is created!")

        # save headers to file
        df.to_csv(self.filename, mode='w', header=True, sep=';', index=False)

    def save_data(self, data):
        # save the incoming data as a line in a csv file
        # print(len(self.headers))
        # print(self.headers)
        # print(data.shape)

        # dataframe, so we know if it fits the data structure
        try:
            df = pd.DataFrame([data], columns=self.headers)
            # print(df)

            # save data to file
            df.to_csv(self.filename, mode='a', header=False, sep=';', index=False)
            # line_terminator="\n")  # without line_terminator windows add a blank line

        except Exception as e:
            print(e)
            print("number of headers probably does not match number of data fields!")

    def save_datalog_array(self, np_array):
        df = pd.DataFrame(np_array, columns=self.headers)
        df.to_csv(self.filename, header=True, sep=';', index=False)

