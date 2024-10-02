import glob
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, TimestampType, FloatType
from textblob import TextBlob  # Make sure to install textblob or use another sentiment analysis library

# Create Spark session
spark = SparkSession.builder \
    .appName("Kafka to CSV with Sentiment Analysis") \
    .getOrCreate()

# Define the schema for the incoming JSON data
schema = StructType() \
    .add("comment", StringType()) \
    .add("video_id", StringType()) \
    .add("timestamp", TimestampType())

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "host.docker.internal:9092") \
    .option("subscribe", "youtube-comments") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse the JSON data
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Define a UDF for sentiment analysis using TextBlob
def get_sentiment(comment):
    return TextBlob(comment).sentiment.polarity

sentiment_udf = udf(get_sentiment, FloatType())

# Add sentiment analysis results to DataFrame
sentiment_df = parsed_df.withColumn("sentiment", sentiment_udf(col("comment")))

# Write the output to a CSV file
output_dir = "data"
checkpoint_dir = "checkpoint"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

query = sentiment_df.writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", output_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .start()

# Await termination
query.awaitTermination()
