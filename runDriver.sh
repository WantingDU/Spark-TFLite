#!/bin/sh
/spark/bin/spark-submit --master spark://10.0.1.9:7078  --class org.apache.spark.examples.SparkPi /spark/examples/jars/spark-examples_2.11-2.4.7.jar 100
