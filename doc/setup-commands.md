### Steps in Detail
* Create an AWS instance and launch it.
* Create docker images using docker-compose file on EC2 machine via ssh
* Create tables in MySQL
* Load the data from MySQL into HDFS storage using Sqoop commands
* Move the data from HDFS to Hive
* Integerate Hive into the Spark
* Extraction of customer demographics information from the data and store it as parquet files using scala implementation
* Move parquet files from Spark to Hive
* Create tables in Hive and load the data from Parquet files into tables.
* Perform Hive analytics on sales and customers demographics data

## Creation of EC2 instance and docker
* Create t2.2xlarge ec2 instance with Amazon Linux 2 AMI (HVM)
```
  Storage: 96GB 
  Allowed Ports: 0-10000
```
 * Connect to the instance using SSH
 ```
 ssh -i "bigdatahiveProject.pem" ec2-user@ec2-43-205-206-126.ap-south-1.compute.amazonaws.com
```
* Install and setup docker and docker-compose
```
sudo yum update -y
sudo yum install docker
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo gpasswd -a $USER docker
newgrp docker
```
* Start docker
```
sudo systemctl start docker
```
* Copy folder from local to ec2 and give required permissions 
(Needs to be done via another command prompt)
```
scp -r -i "bigdatahiveProject.pem" docker_exp ec2-user@ec2-43-205-206-126.ap-south-1.compute.amazonaws.com:/home/ec2-user/docker_exp
sudo chmod -R 755 docker_exp
cd docker_exp
```
* Start docker containers
```
docker-compose up
```
* Port Forwarding to access services locally
(Needs to be done via another command prompt)
```
ssh -i "bigdatahiveProject.pem" ec2-user@ec2-43-205-206-126.ap-south-1.compute.amazonaws.com -o "ServerAliveInterval 30" -L 2081:localhost:2041 -L 4888:localhost:4888 -L 4889:localhost:4889 -L 2080:localhost:2080 -L 8050:localhost:8050 -L 8051:localhost:8051 -L 4141:localhost:4141 -L 4090:localhost:4090 -L 3180:localhost:3180 -L 50075:localhost:50075 -L 50070:localhost:50070 -L 50010:localhost:50010 -L 3077:localhost:3077 -L 4080:localhost:4080 -L 9870:localhost:9870 -L 8188:localhost:8188 -L 9864:localhost:9864 -L 8042:localhost:8042 -L 8088:localhost:8088 -L 8080:localhost:8080 -L 8081:localhost:8081 -L 10000:localhost:10000 -L 6080:localhost:6080 -L 8998:localhost:8998 -L 3306:localhost:3306

```
* Check the status of all running containers and get their ports and names
```
docker ps
```

* To get into the bash shell of different containers
```
docker exec -i -t ra_mysql bash
docker exec -i -t ra_sqoop bash
docker exec -i -t ra_hive-server bash
docker exec -i -t hdp_spark-master bash
docker exec -i -t docker_exp_redis_1 bash
```
* To connect to MySQL Database
```
mysql -u root -p
Password: example
```
* Stop docker containers
```
docker-compose stop
```
* Stop docker
```
sudo systemctl stop docker
```

* Remove docker containers
```
docker-compose down
```
## Hive Spark Dependencies

* Requirements:
1. To ADD Postgresql JAR 
2. Copy hive-site.xml from the hive and put it inside the spark conf directory.

### Steps to add Postgresql JAR 
Steps:
1.1 Download JAR from the internet.
1.2 Commands to copy Jar file from local machine to EC2(Run this command from local machine cmd prompt):
```
scp -r -i "bigdatahiveProject.pem" postgresql-42.3.1.jar ec2-user@ec2-13-127-99-165.ap-south-1.compute.amazonaws.com:/home/ec2-user/
```
1.3 Command to copy file from EC2 into Spark Container under Jars directory
```
docker cp /home/ec2-user/postgresql-42.3.1.jar hdp_spark-master:/spark/jars
```

###  To copy hive-site.xml from the hive and put inside spark conf directory(Run this command from ec2 home directory)
```
docker cp ra_hive-server:/opt/hive/conf/hive-site.xml /home/ec2-user/
docker cp hive-site.xml hdp_spark-master:/spark/conf/hive-site.xml
```
## Loading of sales data by creating testdb database in MySQL
(File Reference: 01_partial_dataset_creation)
Table Creation: 
* Ccard
* Customer_test
* Individual_test
* Salesorderdetail
* Salesorderheader
* Salesperson
* Salesterritory
* Specialoffer
* store

## Creation of views in MySQL
(File Reference: 02_Views Creation)

VIEWS: 
The virtual table in the database
The result set of a stored query
Read-only vs updatable views
Materialized view

ADVANTAGE OF VIEWS: 
To restrict data access
To make complex queries easy
To provide data independence
To present different views of the same data

## Data Ingestion

(File Reference: 03_Sqoop-import)
APACHE SQOOP:
Deals only with structured data to ingest data from RDBMS to the Hadoop cluster

LOADING DATA INTO HIVE TABLES :

(File Reference: 04_Hive_tables_creation(cust, sales, stores))

* Data warehouse software
* Write once and read many times, unlike RDBMS which usually works as read once and writes many times
* Creation of external tables in the hive

## XML Data Processing in Spark
(File Reference: 05_customer_demographic)
* Spark dataframes are immutable by nature (not able to make any changes in the original dataframe)
* Spark work as Lazy evaluation

### Transfering customer_demographic_xml_mined file from Spark to Hive

Firstly, transfer the file from spark to ec2 user
(File Reference: 06_File_copy_commands)
Then, transfer the file from ec2 to hive
```
-rwxr-xr-x 1  1000  1000 6022 Nov 10 08:00 part-00003-cb0266be-53dd-44ce-87c5-2bcea22581c8-c000.snappy.parquet
-rwxr-xr-x 1  1000  1000 5918 Nov 10 08:00 part-00002-cb0266be-53dd-44ce-87c5-2bcea22581c8-c000.snappy.parquet
-rwxr-xr-x 1  1000  1000 5979 Nov 10 08:00 part-00001-cb0266be-53dd-44ce-87c5-2bcea22581c8-c000.snappy.parquet
-rwxr-xr-x 1  1000  1000 5811 Nov 10 08:00 part-00000-cb0266be-53dd-44ce-87c5-2bcea22581c8-c000.snappy.parquet
```

## Creation of tables in Hive and Loading of the data from Parquet files into the tables
(File Reference: 07_customer_demograhics_creation.hql)

## Basic Analysis of Sales Data

* Find the upper and lower discount limits offered for any product 
```
hive> SELECT DISTINCT productid, discountpct
    > FROM sales_order_details sod JOIN sales_order_header soh
    > ON sod.salesorderid = soh.salesorderid
    > ORDER BY productid;
```

* Sales contributions by customer
```
hive> SELECT soh.CustomerID, sum(soh.SubTotal) subtotal, sum(soh.TaxAmt) TaxAmt, sum(soh.Freight) Freight,
    > sum(sod.DiscountPct) discountPercent, sum(soh.TotalDue) TotalDue
    > FROM sales_order_details sod JOIN sales_order_header soh
    > ON sod.salesorderid = soh.salesorderid
    > GROUP BY soh.CustomerID
    > ORDER BY TotalDue desc;

```

* To find the sales contribution by customers on the overall year-to-date sales

```
select customerid, (sum(totalpurchaseytd) over (partition by customerid) / sum(totalpurchaseytd) over ()) percentage from customer_demo cd
order by percentage desc;
```


