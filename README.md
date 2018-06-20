# cloud
TP Cloud Dauphine

# 1. Writing SQL using Spark RDD
Using `Customer.txt` and `Order.txt` stored in the `data` directory.
Write the following SQL queries using Spark RDDs.
- Q1:
```sql
SELECT name
FROM Customer
WHERE month(startDate) = 7
```
- Q2:
```sql
SELECT DISTINCT
    name
FROM Customer
WHERE month(startDate) = 7
```
- Q3:
```sql
SELECT
    O.cid,
    SUM(total),
    COUNT(DISTINCT total)
FROM Order O
GROUP BY O.cid
```
- Q4:
```sql
SELECT
    C.cid,
    O.total
FROM Customer C INNER JOIN Order O on C.cid=O.cid
WHERE C.name LIKE ‘O%’
```

# 2. Run you spark application on AWS Elastic MapReduce
1. Follow the steps given in the document `Tutoriel_AWS_EMR.pdf` to create a Spark cluster.
2. Connect through SSH to the cluster and download the `data` files.
3. Using the scp command, copy your python or scala script to the master node.
4. Still through ssh, submit your application using this command:
```bash
spark-submit my_app.py
```
