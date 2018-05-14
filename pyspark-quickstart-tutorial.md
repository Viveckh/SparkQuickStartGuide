## Install Cloudera
Install VirtualBox and download the Cloudera Quickstart VM

## Allow SSHing
Go to port forwarding in VM Settings and add

* Host IP: 127.0.0.1
* Host Port: 2222
* Guest IP: Find the IP of the cloudera VM instance
* Guest Port: 22

## SSH Credentials
Upon port forwarding, you should be able to SSH into the Cloudera instance with following credentials.

* IP: 127.0.0.1
* Port: 2222
* Username: cloudera
* Password: cloudera

## To see contents in hdfs root
Make sure you are the root user, and then
`hdfs dfs -ls /`
or 
`hadoop fs -ls /`

## To check the status or restart hdfs, if you can't access hdfs
* `service hadoop-hdfs-namenode status`
* `service hadoop-hdfs-namenode restart`

## To disable hdfs safe mode to be able to write contents
`hdfs dfsadmin -safemode leave`

## To check hdfs report
Useful in situations like finding usage and ip, or if it complains about no data node running
* `hdfs dfsadmin -report`

## To start a datanode
`service hadoop-hdfs-datanode start`

## To put files from edge node to hdfs
`hdfs dfs -put localfilepath hdfspath`
or
`hadoop fs -put localfilepath hdfspath`

## To submit Spark program to run in cluster
`spark-submit --master yarn-client --packages thedependencypackagenameshere path/to/file/pi.py`

## To list and kill running YARN applications
`yarn application -list` to view running applications
`yarn application -kill <id>` to kill the application with the given id

## Some Useful Spark functions to get started
* sc.parallelize
> Forms a distributed dataset so they can be operated on in parallel
```python
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)
```

*sc.accumulator
> Accumulators are variables that are only “added” to through an associative and commutative operation and can therefore be efficiently supported in parallel. They can be used to implement counters (as in MapReduce) or sums. Spark natively supports accumulators of numeric types, and programmers can add support for new types.
```python
>>> accum = sc.accumulator(0)
>>> accum
Accumulator<id=0, value=0>

>>> sc.parallelize([1, 2, 3, 4]).foreach(lambda x: accum.add(x))
...
10/09/29 18:41:08 INFO SparkContext: Tasks finished in 0.317106 s

>>> accum.value
10
```

* map
> applies a function to all the items in an input_list
```python
map(function_to_apply, list_of_inputs)

items = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, items))
```

* reduce
> useful function for performing some computation on a list and returning the result. It applies a rolling computation to sequential pairs of values in a list. For example, if you wanted to compute the product of a list of integers.
```python
product = reduce((lambda x, y: x * y), [1, 2, 3, 4])
```

* filter
> creates a list of elements for which a function returns true
```python
less_than_zero = list(filter(lambda x: x < 0, number_list))
```

* flatmap
> Return a new RDD by first applying a function to all elements of this RDD, and then flattening the results
```python
>>> rdd = sc.parallelize([2, 3, 4])
>>> sorted(rdd.flatMap(lambda x: range(1, x)).collect())
[1, 1, 1, 2, 2, 3]
>>> sorted(rdd.flatMap(lambda x: [(x, x), (x, x)]).collect())
[(2, 2), (2, 2), (3, 3), (3, 3), (4, 4), (4, 4)]
```

* groupbykey
> Group the values for each key in the RDD into a single sequence. Hash-partitions the resulting RDD with numPartitions partitions.
```python
>>> rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
>>> sorted(rdd.groupByKey().mapValues(len).collect())
[('a', 2), ('b', 1)]
>>> sorted(rdd.groupByKey().mapValues(list).collect())
[('a', [1, 1]), ('b', [1])]
```
 
* reducebykey
Merge the values for each key using an associative and commutative reduce function
```python
>>> from operator import add
>>> rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
>>> sorted(rdd.reduceByKey(add).collect())
[('a', 2), ('b', 1)]
```

* fold
Aggregate the elements of each partition, and then the results for all the partitions, using a given associative function and a neutral “zero value.”
```python
>>> from operator import add
>>> sc.parallelize([1, 2, 3, 4, 5]).fold(0, add)
15
```
* show
Prints the contents of a dataframe. You can pass an optional parameter of 'n' to specify the number of rows to print
```python
>>> df.show(n=2)
```

## Useful Links
* https://www.analyticsvidhya.com/blog/2016/10/spark-dataframe-and-operations/