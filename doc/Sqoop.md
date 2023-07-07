## Sqoop

Sqoop is a tool used to transfer the data from 
* RDBMS to HDFS
* HDFS to RDBMS

Sqoop is also a mapreduce job where only mappers work, no reducer is required as we just need to transfer the data, no as such aggregation needed.

By default, the number of mappers in Sqoop import is 4 but if user wants, he/she can change the number.
* Sqoop Import(Data Ingestion): used to transfer the data from RDBMS to HDFS
* Sqoop Export(Data Migration): used to transfer the data from HDFS to RDBMS

![Sqoop](https://user-images.githubusercontent.com/29665085/202442597-67af3183-0746-40c3-af39-ce9e2b8807fe.png)
