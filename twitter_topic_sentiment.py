import json
import sys
import pyspark
from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# initialize spark

import os

#os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-8-openjdk-amd64/'

# setup arguments
#os.environ['SPARK_HOME'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0'

import findspark
findspark.init('C:/spark-2.4.7-bin-hadoop2.7')

def fun(avg_senti_val):
    try:
        if avg_senti_val < 0: return 'NEGATIVE'
        elif avg_senti_val == 0: return 'NEUTRAL'
        else: return 'POSITIVE'
    except TypeError:
        return 'NEUTRAL'

if __name__ == "__main__":

    schema = StructType([                                                                                          
        StructField("text", StringType(), True),
        StructField("senti_val", DoubleType(), True)    
    ])
    
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis")\
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:2.4.7')\
    .getOrCreate()
   

    kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "twitter").load()

    kafka_df_string = kafka_df.selectExpr("CAST(value AS STRING)")

    tweets_table = kafka_df_string.select(from_json(col("value"), schema).alias("data")).select("data.*")

    sum_val_table = tweets_table.select(avg('senti_val').alias('avg_senti_val'))
    
    # udf = USER DEFINED FUNCTION
    udf_avg_to_status = udf(fun, StringType())

    # avarage of senti_val column to status column
    new_df = sum_val_table.withColumn("status", udf_avg_to_status("avg_senti_val"))

    query = new_df.writeStream.outputMode("complete").format("console").start()

    query.awaitTermination()
