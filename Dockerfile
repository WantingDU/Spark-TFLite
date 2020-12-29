 FROM arm32v7/openjdk:8

 RUN apt-get update && apt-get install -y wget
 RUN apt-get update && apt-get install -y tar
 RUN apt-get update && apt-get install -y bash
 RUN wget https://archive.apache.org/dist/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz
 RUN tar -zxvf spark-2.4.7-bin-hadoop2.7.tgz
 RUN mv spark-2.4.7-bin-hadoop2.7 /spark
 RUN apt-get install -y python3 python3-pip
 ENV PYTHONPATH  $/spark/python:$/spark/python/lib/py4j-0.10.7-src.zip


 COPY runWorker.sh .
 RUN chmod 777 /runWorker.sh
 COPY runMaster.sh .
 RUN chmod 777 /runMaster.sh
 COPY runDriver.sh .
 RUN chmod 777 /runDriver.sh

# install git 

# install git 
RUN apt-get update && \ 
apt-get upgrade -y && \ 
apt-get install -y git


 RUN git clone https://github.com/WantingDU/Spark-TFLite
 RUN pip3 install --requirement /Spark-TFLite/reqstf.txt