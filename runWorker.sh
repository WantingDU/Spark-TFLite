#!/bin/sh
./spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://10.0.1.9:7078 -c 2 -m 200m
