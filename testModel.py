import os
import csv
from NeuralLibrary import NeuralModel

from __future__ import print_function
import sys
from random import random
from operator import add
from pyspark.sql import SparkSession

def main():
    spark = SparkSession\
        .builder\
        .appName("PredictTemperature")\
        .getOrCreate()
    data_path="./jena_weather_dataset_roof.csv"
    #data_raw = data_from_file(data_path)
    
    # Specify which model to use
    model = NeuralModel("./model_bilstm.tflite")

    # Format data
    #input_data = model.input_data(data_raw)

    # print("Output details:", model.get_details()[1])

    # Run the model with input data
    output=spark.read.csv(data_path).rdd.map(lambda i:model.input_data(i)).parallelize(range(1, 2), 1).map(lambda m:model.run(m)) #problem: where to place inputdata(m)
    #output = model.run(input_data)
    print("*********\nOutput =\n")
    print(output)



if __name__ == '__main__':
    main()