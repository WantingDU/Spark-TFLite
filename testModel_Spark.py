
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
    #data_raw = data_from_file(data_path)
    
    # Specify which model to use
    model = NeuralModel("/Spark-TFLite/model_bilstm.tflite")

    # Format data
    #input_data = model.input_data(data_raw)

    # print("Output details:", model.get_details()[1])

    # Run the model with input data
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    print("000000000000000000000000")
    #df = spark.read.csv(data_path).select('*').toPandas()
    df = pd.read_csv(data_path)
    #csv_stream = spark.sparkContext.parallelize([csv_str.collect()[0][1]]).collect().map(lambda data:StringIO(data))
    #df = csv_str.map(lambda data: pd.read_csv(data))
    print("11111111111111111111111111")
    df_rdd = spark.sparkContext.parallelize([df])
    print("yooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    input_rdd = df_rdd.map(lambda i: NeuralModel("/Spark-TFLite/model_bilstm.tflite").input_data(i))
    print("2222222222222222222222222222")
    output_rdd = input_rdd.map(lambda m: NeuralModel("/Spark-TFLite/model_bilstm.tflite").run(m))
    print("shaaaaaaaaaaaaaaaaaaaaaaaaaabiiiiiiiiiiiiiiiiiiiiii=======================")
    output = output_rdd.collect()
    for x in output:
        print(x[0])
    #output=spark.read.csv(data_path).rdd.map(lambda r: r[0]).flatMap(lambda x:x.split('')).map(lambda i: NeuralModel("/Spark-TFLite/model_bilstm.tflite").input_data(i[0])).map(lambda m: NeuralModel("/Spark-TFLite/model_bilstm.tflite").run(m)) #problem: where to place inputdata(m)
    #output = model.run(input_data)
    print("***********************\nOutput =\n")
    #print(output)



if __name__ == '__main__':
    main()
