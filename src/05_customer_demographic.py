from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# Create SparkSession
spark = SparkSession.builder.getOrCreate()

# Read data from Hive table
hive_df = spark.sql("select * from default.customer_test")

# Select relevant columns
projDF = hive_df.select("CustomerID", "Demographics")

# Define schema for CustomerDemo
schema = StructType([
    StructField("CustomerID", IntegerType(), nullable=True),
    StructField("TotalPurchaseYTD", StringType(), nullable=True),
    StructField("DateFirstPurchase", StringType(), nullable=True),
    StructField("BirthDate", StringType(), nullable=True),
    StructField("MaritalStatus", StringType(), nullable=True),
    StructField("YearlyIncome", StringType(), nullable=True),
    StructField("Gender", StringType(), nullable=True),
    StructField("TotalChildren", StringType(), nullable=True),
    StructField("NumberChildrenAtHome", StringType(), nullable=True),
    StructField("Education", StringType(), nullable=True),
    StructField("Occupation", StringType(), nullable=True),
    StructField("HomeOwnerFlag", StringType(), nullable=True),
    StructField("NumberCarsOwned", StringType(), nullable=True),
    StructField("CommuteDistance", StringType(), nullable=True)
])

# Define function to parse XML and create CustomerDemo objects
def createCustDemo(row):
    custId = int(row.CustomerID)
    demo = row.Demographics
    node = ET.fromstring(demo)
    return (custId,
            (node.find(".//TotalPurchaseYTD").text if node.find(".//TotalPurchaseYTD") is not None else None),
            (node.find(".//DateFirstPurchase").text if node.find(".//DateFirstPurchase") is not None else None),
            (node.find(".//BirthDate").text if node.find(".//BirthDate") is not None else None),
            (node.find(".//MaritalStatus").text if node.find(".//MaritalStatus") is not None else None),
            (node.find(".//YearlyIncome").text if node.find(".//YearlyIncome") is not None else None),
            (node.find(".//Gender").text if node.find(".//Gender") is not None else None),
            (node.find(".//TotalChildren").text if node.find(".//TotalChildren") is not None else None),
            (node.find(".//NumberChildrenAtHome").text if node.find(".//NumberChildrenAtHome") is not None else None),
            (node.find(".//Education").text if node.find(".//Education") is not None else None),
            (node.find(".//Occupation").text if node.find(".//Occupation") is not None else None),
            (node.find(".//HomeOwnerFlag").text if node.find(".//HomeOwnerFlag") is not None else None),
            (node.find(".//NumberCarsOwned").text if node.find(".//NumberCarsOwned") is not None else None),
            (node.find(".//CommuteDistance").text if node.find(".//CommuteDistance") is not None else None)
            )

# Apply createCustDemo function to each row and create DataFrame
projRDD = projDF.rdd.map(createCustDemo)
projDF = projRDD.toDF(schema)

# Write DataFrame to Parquet format
projDF.write.format("parquet").mode("append").save("customer_demographics_xml_mined")
