from pyspark.sql import SparkSession, Window
from pyspark.sql.types import *
from pyspark.sql.functions import *

#creating a spark session
def sparkSession():
    spark=SparkSession.builder.getOrCreate()
    return spark

#creating a dataframe
def dataFrame_creation(spark):
    data=[("James","Sales",3000),
      ("Michael","Sales",4600),
      ("Robert","Sales",4100),
      ("Maria","Finance",3000),
      ("Raman","Finance",3000),
      ("Scott","Finance",3300),
      ("Jen","Finance",3900),
      ("Jeff","Marketing",3000),
      ("Kumar","Marketing",2000)]
    schema=StructType([StructField("EmpName",StringType(),True),
                   StructField("Department",StringType(),True),
                   StructField("Salary",IntegerType(),True)])
    df=spark.createDataFrame(data=data, schema=schema)
    return df
#to find the first row in each department (by grouping department column)
#to select the first row in each group, we use window partitionBy() and row_number() funtcion.
#import window for using this function
def first_row_dept_wise(df):
    window1=Window.partitionBy("Department").orderBy("Salary")
    #default sorting order is ascending, so it shows the lowest salary and corresponding person name,dept in result
    df1=df.withColumn("row",row_number().over(window1)).filter(col("row")==1).drop("row")
    return df1

#retrieving highest salaried person in each group
def highest_sal_dept_wise(df):
    window2=Window.partitionBy("Department").orderBy(col("Salary").desc())
    df1=df.withColumn("row",row_number().over(window2)).filter(col("row")==1).drop("row")
    return df1

#each department wise selecting the highest, lowest, average and total_salary.
def high_low_avg_totSal(df):
    window3=Window.partitionBy("Department").orderBy("Salary")
    real_data=Window.partitionBy("Department")
    df1=df.withColumn("row",row_number().over(window3))\
            .withColumn("Average",avg(col("Salary")).over(real_data))\
            .withColumn("highest_salary",max(col("Salary")).over(real_data))\
            .withColumn("lowest_salary",min(col("Salary")).over(real_data))\
            .withColumn("total_salary",sum(col("Salary")).over(real_data))\
            .where(col("row")==1).drop("row").select("Department","Average","highest_salary","lowest_salary","total_salary")
    return df1