from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TwitterDataAnalysis") \
    .getOrCreate()

filePath = "hdfs:///path/to/data/twitter-50mb.json"
lines = spark.sparkContext.textFile(filePath)

import re

def extract_info(line):
    created_at_match = re.search(r'"created_at":"(.*?)"', line)
    sentiment_match = re.search(r'"sentiment":([-\d.]+)', line)
    
    created_at = created_at_match.group(1) if created_at_match else None
    sentiment = float(sentiment_match.group(1)) if sentiment_match else 0
    
    return (created_at, sentiment)

extracted_info = lines.map(extract_info)

from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql import Row

schema = StructType([
    StructField("created_at", StringType(), True),
    StructField("sentiment", FloatType(), True)
])

row_rdd = extracted_info.map(lambda x: Row(created_at=x[0], sentiment=x[1]))

df = spark.createDataFrame(row_rdd, schema)

from pyspark.sql.functions import to_timestamp, to_date, hour, avg, col
df = df.withColumn("timestamp", to_timestamp("created_at", "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"))
df = df.withColumn("date", to_date("timestamp"))
df = df.withColumn("hour", hour("timestamp"))



from pyspark.sql.functions import avg

# hour avg
happiest_hour_df = df.groupBy("date", "hour").agg(avg("sentiment").alias("avg_sentiment"))
# highest hour
happiest_hour = happiest_hour_df.orderBy(col("avg_sentiment").desc()).first()

# 按天计算平均情感得分
happiest_day_df = df.groupBy("date").agg(avg("sentiment").alias("avg_sentiment"))
# 找出情感得分最高的一天
happiest_day = happiest_day_df.orderBy(col("avg_sentiment").desc()).first()


# 按小时计算推文数量
most_active_hour_df = df.groupBy("date", "hour").count()
# 找出推文数量最多的小时
most_active_hour = most_active_hour_df.orderBy(col("count").desc()).first()

# 按天计算推文数量
most_active_day_df = df.groupBy("date").count()
# 找出推文数量最多的一天
most_active_day = most_active_day_df.orderBy(col("count").desc()).first()

