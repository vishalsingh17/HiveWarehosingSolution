## Hive
Hive is an open source Data Warehouse tool to process structured data on top of Hadoop which is meant to solve the analytical problems.

### Transactional System
It is the one which basically deals with the transactions related to day to day data. It deals with present data.
*	It analyzes individual entries
* Access to recent data, from the last few hours or days
* In such system we used to insert, update the data
*	Fast real-time access
*	Usually a single data source
*	for example : ATM

Traditional RDBMS( Oracle, MySql) Databases are best suited for transactional system.

Monolithic System is best suited to design transactional system.	

### Analytical System
It is the one where we deal with historical data.
* It analyzes large batches of data
* Access to older data going back months or even years
* In such system we mostly talk about reads
*	Long running jobs
*	Multiple data sources
*	for example : I want to analyse why are the sales less in this month
 
Data warehouse(teradata, vertica, oracle, IBM) are best suited for analytical systems.

### Features of Data Warehouse
*	Long running batch jobs
*	Optimized for read operations
*	Holds data from multiple sources
*	Holds data over a long period of time
*	Data may be lagged, not real time

### Hive is an abstraction on top of MapReduce
![Hive Architecture@1 25x](https://user-images.githubusercontent.com/29665085/202446272-6b0bcc1a-af7d-4949-af36-2d4c88a72966.png)

### Importance of Hive
As a developer we will write some SQL like queries (Hive Query Language) then Hive will convert these queries as a MapReduce Job and will submit on the Hadoop Cluster. 

### Why not traditional database but hive?
Traditional databases are monolithic system which doesn't provide parallelism but Hive is a distributed system which provides parallelism.
We will be visualizing the data in the form of tables.

Hive table has two parts :
* Actual Data - stored in HDFS in the form of files
* Metadata ( Schema ) - stored in a Database ( Derby By default )

