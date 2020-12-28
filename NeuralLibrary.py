#!/usr/bin/python
# coding=utf-8

import datetime
import tensorflow as tf
#import tflite_runtime.interpreter as tflite
import numpy as np
import pandas as pd


class NeuralModel():
    def __init__(self, model_path):
        # Load the TFLite model and allocate tensors.
        self.interpreter = tf.lite.Interpreter(model_path)
        self.interpreter.allocate_tensors()

        # Get input and output tensors.
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
        self.output_shape = self.output_details[0]['shape']

        self.tmean = pd.read_csv('Datasets/train_mean.csv')
        self.tstd = pd.read_csv('Datasets/train_std.csv')
        self.tmean = self.tmean.iloc[0] #permet de récupérer l'objet sous forme de série 
        self.tstd = self.tstd.iloc[0]

    def run(self, data):
        print("input data length:",len(data))
        print("input shape:", self.input_shape)
        print("output shape:", self.output_shape)

        self.interpreter.set_tensor(self.input_details[0]['index'], data)
        self.interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        rtensor = self.interpreter.get_tensor(self.output_details[0]['index'])
        return self.output_data(rtensor)

    def input_data(self, df, type="JENA"):
        if (type == "JENA"):
            df = df[5::6]
            if(len(df)<self.input_shape[1]):
                diff = self.input_shape[1]-len(df)
                print("Detected", diff, "missing values, [completing with duplicated values] <- not implemented yet")
                # Implement missing values completion...
            date_time = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')

        df.head()
        timestamp_s = date_time.map(datetime.datetime.timestamp)
        day = 24 * 60 * 60
        year = (365.2425) * day

        df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
        df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

        df = df[:self.input_shape[1]]

        # Normalization:
        print("Before normalization:")
        print("df:\n",df)
        print("mean:\n",self.tmean)
        print("std:\n",self.tstd)

        df = (df - self.tmean) / self.tstd

        print("After normalization, df:\n",df)

        data = np.array(df, dtype=np.float32)
        data = [data]
        return data

    def get_details(self):
        return self.input_details, self.output_details

    def get_input_shape(self):
        return self.input_shape

    def output_data(self, data):
        out = []
        for item in data:
            print(self.tstd.keys())
            # TODO this is a VERY ugly workaround to use .keys()[1] to get temp but due to how pandas writes keys I couldn't find better
            out.append(item * float(self.tstd.keys()[1]) + float(self.tmean.keys()[1]))
        return out


### Normalization des donnees ###
"""
train_data_mean = train_data.mean() <-- Moyennage
train_data_std = train_data.std() <-- Déviation standard

Equation de normalization

train_data = (train_data - train_data_mean)/train_data_std <-- Normalization
"""

### Denormalization des donnees ###
"""
Equation de denormalization

denormalized_data = predicted_value * train_data_std + train_data_mean <-- Denormalization
d = p *  8.028711 + 286.562641
"""
