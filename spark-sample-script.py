# A sample pySpark script for reference
# Author: Vivek Pandey

# This script reads a trip history of bikes in NYC for a given month from HDFS, 
# filters the 90s kids, and exaggerates their trip duration and writes it to a file
# PREREQUISITES: MAKE SURE THE INPUT FILE EXISTS IN /user/cloudera/ in HDFS

# To run this script standalone
# spark-submit --packages com.databricks:spark-csv_2.10:1.4.0 sparktutorial.py

# To run the commands one by one in shell mode, launch pyspark shell with command
# pyspark --packages com.databricks:spark-csv_2.10:1.4.0
# Execute the steps one at a time, no need to do the imports and context initialization part and convert all functions to lambda functions

# PROGRAM BEGINS HERE

# Import dependencies and initialize sparkContext and sqlContext
# This part is not necessary if you are executing these commands in pyspark shell mode.
# In shell mode, you are provided with a default 'sc' SparkContext and SqlContext
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext()
sqlContext = SQLContext(sc)

# This function just increments the global accumulator by 1 everytime it is called and doubles the input number
def exaggerateTripDuration(x):
    global accum
    accum.add(1)
    return x * 2

# Read from csv using path from hdfs root
df = sqlContext.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load('/user/cloudera/201702-citibike-tripdata.csv')

# Printing schema
df.printSchema()

# Showing dataframe, where n is the number of rows to display
df.show(n=2)
print("TOTAL RECORDS ", df.count())

# Filter dataframe records with 90s kids
filteredf = df.filter((df['Birth Year'] >= 1990) & (df['Birth Year'] < 2000))

# Selecting only a few column(s), as a dataframe
selectedf = filteredf.select("Trip Duration", "Start Station ID", "End Station ID", "Bike ID", "User Type", "Birth Year", "Gender")
selectedf.show()
print("TOTAL 90s kids ", selectedf.count())

#Writing a dataframe to external file in hdfs. The output folder will contain the files with the results
selectedf.write.format("com.databricks.spark.csv").mode('overwrite').save("/user/cloudera/whodat")

#WORKING WITH PARALLEL PROCESSING

# Storing selected column as a list, and parallelizing results. Don't use for selecting multiple columns, since it flattens all of the values into a single array
selectedList = df.select("Trip Duration").rdd.flatMap(list).collect()

# Create a parallelized collection whose elements can be operated in parallel
parallelizedRDD = sc.parallelize(selectedList)

# Create an accumulator which can maintain variables like counters across threads while processes are running in parallel
accum = sc.accumulator(0)

# Operate on the parallelized collection
parallelizedRDD.foreach(exaggerateTripDuration)

parallelizedRDD.take(20)

# The following two numbers should match
print("ACCUMULATOR ", accum)
print("ENTRIES IN PARALLELIZED RDD ", parallelizedRDD.count())