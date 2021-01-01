import os
import csv
from NeuralLibrary import NeuralModel
import numpy as np
import pandas as pd

def main():
    data_raw = data_from_file("./Datasets/Jena/jena_weather_dataset_roof.csv")
    
    # Specify which model to use
    model = NeuralModel("./model_bilstm.tflite")

    # Format data
    input_data = model.input_data(data_raw)

    # print("Output details:", model.get_details()[1])

    # Run the model with input data
    output = model.run(input_data)
    print("*********\nOutput =\n")
    print(output)

def data_from_file(data_path):
    data = pd.read_csv(data_path)

    return data


if __name__ == '__main__':
    main()
