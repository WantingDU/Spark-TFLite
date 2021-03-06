 FROM arm32v7/openjdk:8

 # For debugging, to delete when going into production
 RUN apt-get update && apt-get install -y vim

 # Install python3
 COPY --from=arm32v7/python:3.7-slim-buster / /
 RUN pip3 install numpy pandas --extra-index-url https://www.piwheels.org/simple
 # install tflite-runtime for armv7
 RUN pip3 install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp37-cp37m-linux_armv7l.whl
 
 # Install shared dependencies
 RUN apt-get update && apt-get install -y libblas3 liblapack3 liblapack-dev libblas-dev libatlas-base-dev

 # Install Spark
 RUN wget https://archive.apache.org/dist/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz
 RUN mkdir /spark && tar -zxvf spark-2.4.7-bin-hadoop2.7.tgz --strip 1 -C /spark
 # Set PYTHONPATH
 ENV PYTHONPATH /spark/python:/spark/python/lib/py4j-0.10.7-src.zip:$PYTHONPATH

 # Downloading scripts
 RUN wget https://github.com/WantingDU/Spark-TFLite/tarball/main
 RUN mkdir /Spark-TFLite && tar -xf main --strip 1 -C /Spark-TFLite
 
 RUN mv /Spark-TFLite/*.sh /
 RUN chmod 777 /runWorker.sh && chmod 777 /runMaster.sh && chmod 777 /runDriver.sh
