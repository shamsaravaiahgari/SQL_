
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from utils_sql_1 import *

#creationg a spark session
spark=spark_session()

#creating a dataFrame with the given data
df1=create_dataFrame(spark)

#Extracting the firstName,lastName,salary column from the dataFrame
fname_lname_sal=select_columns(df1)

#printing the name of the person who has maximum salary
max_sal_name=max_salary(df1)

#adding age,department,country as three new columns
add_country_age_dept=adding_new_columns(df1)

#dropping the age and department columns
drop_age_dept=drop_age_dept_columns(add_country_age_dept)

#getting the distinct values from dob column
dob_distinct=distinct_values_dob(df1)

#getting the distinct values from salary column
salary_distinct=distinct_values_salary(df1)

#updating the value of salary column
new_salary_df=new_salary(df1)

#converting the datatypes of dob and salary columns
DataType_conversion=converting_dataTypes(df1)

#renaming the nested column names
rename_nested_column=renaming_nested_column(df1)

#updating the salary value by 5000 and adding it as new column
new_salary_col=deriving_new_col_sal(df1)
