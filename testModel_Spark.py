
import os
import csv
from NeuralLibrary import NeuralModel
import numpy as np
import pandas as pd

import sys
from random import random
from operator import add
from pyspark.sql import SparkSession


    
def main():
    spark = SparkSession\
        .builder\
        .appName("PredictTemperature")\
        .getOrCreate()
    data_path="/Spark-TFLite/jena_weather_dataset_roof.csv"

    
    # Specify which model to use
    model = NeuralModel("/Spark-TFLite/model_bilstm.tflite")


    # Run the model with input data
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    df = pd.read_csv(data_path)
    df_rdd = spark.sparkContext.parallelize([df])
    input_rdd = df_rdd.map(lambda i: NeuralModel("/Spark-TFLite/model_bilstm.tflite").input_data(i))
    output_rdd = input_rdd.map(lambda m: NeuralModel("/Spark-TFLite/model_bilstm.tflite").run(m))
    output = output_rdd.collect()
    for x in output:
        print(x[0])

    print("***********************\nOutput =\n")




if __name__ == '__main__':
    main()
