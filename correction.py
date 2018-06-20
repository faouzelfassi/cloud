cust_file = sc.textFile("hdfs:///user/hadoop/Customer.txt")
order_file = sc.textFile("hdfs:///user/hadoop/Order.txt")

# q1:
# SELECT name FROM Customer WHERE month(startDate)=7

names = cust_file.filter(lambda x: "/07/" in x).map(lambda x: x.split(",")[2])
names.collect()

# q2:
# SELECT DISTINCT name FROM Customer WHERE month(startDate) = 7

# In order to print only the first name we can add another split within the same map
names = cust_file.filter(lambda x: "/07/" in x).map(lambda x: x.split(",")[2].split(" ")[0]).distinct()
names.collect()

# q3:
# SELECT O.cid, SUM(total), COUNT(DISTINCT total) FROM Order O GROUP BY O.cid

# An array can't be reduced, we need to define the key and the value of the RDD,
# here the key is cid (1st col) and the value is total (2nd col)
total_per_cust = order_file.map(lambda x: x.split(",")).map(lambda a: (a[0], int(a[1]))).reduceByKey(lambda a, b: a + b)

# And here we count the number of unique record per cid:
# First I create an RDD where the key is the pair (cid, total), and the value 1
cid_total = order_file.map(lambda x: x.split(",")).map(lambda a: ((a[0], a[1]), 1)).distinct()
# This way we can sum the unique totals associated with the key - the map extract the cid as a key from the pair (cid, total), and the 1 as a value.
count_cid_total = cid_total.map(lambda a: (a[0][0], a[1])).reduceByKey(lambda a, b: a + b)
# We join the two RDDs in order to have the cid, sum(total), count(distinct total)
total_count_per_cust = total_per_cust.join(count_cid_total).collect()

# q4:
# SELECT C.cid, O.total FROM Customer C, Order O WHERE C.name LIKE ‘O%’ and C.cid=O.cid

# After filtering the names starting with 'O',
# I create a key value pair with the key: cid and value: name in order to use joins
# because the two RDD must have the same signature: [String, String]
cust_map = cust_file.map(lambda x: x.split(",")).filter(lambda x: x[2].startswith("O")).map(lambda a: (a[0], a[2])).distinct()
order_map = order_file.map(lambda x: x.split(",")).map(lambda a: (a[0], a[1]))
# We join the two RDD on the key
cust_orders = cust_map.join(order_map)
cust_orders.collect()
