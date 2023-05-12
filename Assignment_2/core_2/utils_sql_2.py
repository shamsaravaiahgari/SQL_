from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

#creating a spark session
def spark_creation():
    spark = SparkSession.builder.getOrCreate()
    return spark

#creating a dataframe
def create_dataFrame(spark):
    data = [("Banana",1000,"USA"),
        ("Carrots",1500,"India"),
        ("Beans",1600,"Sweden"),
        ("Orange",2000,"UK"),
        ("Orange",2000,"UAE"),
        ("Banana",400,"China"),
        ("Carrots",1200,"China")]
    Schema=StructType([ StructField("Product",StringType(),True),
                   StructField("Amount",IntegerType(),True),
                   StructField("Country",StringType(),True) ])
    df=spark.createDataFrame(data=data, schema=Schema)
    return df

#creating a pivot table
def func_pivot(df):
#pivot is used to transpose the rows to columns
#total amount exported to each country under each product
    pivot_df=df.groupBy("Product").pivot("country").sum("Amount")
    return pivot_df

#creating unpivot table
def func_unpivot(pivot_df):
#unpivot is reverse of pivot
#transposing columns into rows, done by using stack() function
    unpivot_df=pivot_df.select("Product", expr("stack(6, 'china', China, 'india', India, 'sweden', Sweden, 'uae', UAE,'uk',UK,'usa',USA) \
            as (country, Total)")).where("Total is not null")
    return unpivot_df