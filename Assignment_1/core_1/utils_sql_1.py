from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

#to create the spark session
def spark_session():
    spark = SparkSession.builder.getOrCreate()
    return spark

#df using provided data
def create_dataFrame(spark):
    data=[  ({"firstname":"James","middlename":"","lastname":"Smith"},"03011998","M",3000),
        ({"firstname":"Michael","middlename":"Rose","lastname":""},"10111998","M",20000),
        ({"firstname":"Robert","middlename":"","lastname":"Williams"},"02012000","M",3000),
        ({"firstname":"Maria","middlename":"Anne","lastname":"Jones"},"03011998","F",11000),
        ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"}, "04101998", "M", 10000)  ]
    #schema of the df
    Schema=StructType([StructField("name",MapType(StringType(),StringType()),True),
                   StructField("dob",StringType(),True),
                   StructField("gender",StringType(),True),
                   StructField("salary",IntegerType(),True)])
    df=spark.createDataFrame(data=data,schema=Schema)
    return df

#Extracting the firstName,lastName,salary column from the dataFrame
def select_columns(df):
    #printing the firstname and lastname with their respective salary
    #df.rdd returns the RDD
    #The map operation is applied to the RDD returned by df.rdd. The map operation applies a given function to each element of the RDD and returns a new RDD consisting of the results
    return df.rdd.map(lambda x:(x.name["firstname"],x.name["lastname"],x.salary)).toDF(["firstname","lastname","salary"])

#printing the name of the person who has maximum salary
def max_salary(df):
    def max_salary(df):
        # Sort the DataFrame in descending order by the 'salary' column
        df3 = df.sort(col("salary").desc())
        # Select the first row of the sorted DataFrame
        df5 = df3.limit(1)
        # Select the 'name' column from the row
        df6 = df5.select("name")
        # Return the DataFrame with the 'name' column
        return df6

#adding age,department,country as three new columns
def adding_new_columns(df):
    df1=df.withColumn("country",lit(None)).withColumn("department",lit(None)).withColumn("age",lit(None))
    return df1

#dropping the age and department columns
def drop_age_dept_columns(df):
    return df.drop("department","age")

#getting the distinct values from salary column
def distinct_values_salary(df):
    return df.select(col("salary")).distinct()

#getting the distinct values from dob column
def distinct_values_dob(df):
    return df.select(col("dob")).distinct()

#updating the value of salary column by 1000
def new_salary(df):
    return df.withColumn("salary",col("salary")+1000)

#converting the datas type of columns dob and salary to string
def converting_dataTypes(df):
    return df.withColumn("dob",col("dob").cast(StringType())).withColumn("salary",col("salary").cast(StringType()))

#renaming the nested name column
def renaming_nested_column(df):
    df4 = df.withColumn("fname", col("name.firstname")) \
        .withColumn("mname", col("name.middlename")) \
        .withColumn("lname", col("name.lastname")) \
        .drop("name")
    return df4

#updating the salary value by 5000 and adding it as new column
def deriving_new_col_sal(df):
    return df.withColumn("new_col_salary",col("salary")+5000)



