from Assignment_1.core_1.utils_sql_1 import *
import unittest

class TestMyFunc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark=( SparkSession.builder.master("local[*]").appName("test").getOrCreate() )
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

# Testing DataFrame
    def testdataframe(self):
        #creating a dataFrame
        data = [({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M", 3000),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M", 20000),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M", 3000),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F", 11000),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F", 10000)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                             StructField("dob", StringType()),
                             StructField("gender", StringType()),
                             StructField("salary", IntegerType())])
        df = self.spark.createDataFrame(data=data,schema=schema)


        #testing of selecting firstName,lastName, salary columns
        data = [("James", "Smith", 3000),
                ("Michael", "", 20000),
                ("Robert", "Williams", 3000),
                ("Maria", "Jones", 11000),
                ("Jen", "Brown", 10000)]
        schema = StructType([StructField("name[firstname]", StringType()),
                             StructField("name[lastname]", StringType()),
                             StructField("salary", IntegerType())])
        expected_df = self.spark.createDataFrame(data, schema)
        transformed_df=select_columns(df)
        self.assertEqual(expected_df.collect(),transformed_df.collect())

        #testing of adding new columns country,age,department
        data = [
            ({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M", 3000, None, None, None),
            ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M", 20000, None, None, None),
            ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M", 3000, None, None,None),
            ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F", 11000, None, None,None),
            ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F", 10000, None, None,None)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                             StructField("dob", StringType()),
                             StructField("gender", StringType()),
                             StructField("salary", IntegerType()),
                             StructField("country", StringType()),
                             StructField("department", StringType()),
                             StructField("age", StringType())])
        expected_df = self.spark.createDataFrame(data, schema)
        df1=self.spark.createDataFrame(data, schema)
        transformed_df = adding_new_columns(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())

        #testing of changing the value of salary column
        data = [
                ({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M",4000),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M",21000),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M",4000),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F",12000),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F",11000)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                                 StructField("dob", StringType()),
                                 StructField("gender", StringType()),
                                 StructField("salary", IntegerType())])
        expected_df = self.spark.createDataFrame(data, schema)
        df_new=self.spark.createDataFrame(data, schema)
        transformed_df = new_salary(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())

        #testing converting datatypes
        data = [({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M", 3000),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M", 20000),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M", 3000),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F", 11000),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F", 10000)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                                 StructField("dob", StringType()),
                                 StructField("gender", StringType()),
                                 StructField("salary", StringType()),
                                 ])
        expected_df = self.spark.createDataFrame(data, schema)
        transformed_df = converting_dataTypes(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())


        # testing of creation of new column as new_col_salary with value salary+5000
        data = [
                ({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M", 4000,9000),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M", 21000,26000),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M", 4000,9000),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F", 12000,17000),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F", 11000,16000)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                                 StructField("dob", StringType()),
                                 StructField("gender", StringType()),
                                 StructField("salary", IntegerType()),
                                 StructField("new_col_salary", IntegerType())])
        expected_df = self.spark.createDataFrame(data, schema)
        transformed_df = deriving_new_col_sal(df_new)
        self.assertEqual(expected_df.collect(), transformed_df.collect())

        # testing the renaming of a nested column
        data = [
                ("03011998", "M", 4000,"James",  "",  "Smith"),
                ("10111998", "M", 21000,"Michael",  "Rose",  ""),
                ("02012000", "M", 4000, "Robert", "",  "Williams"),
                ("03011998", "F", 12000, "Maria",  "Anne",  "Jones"),
                ("04101998", "F", 11000,"Jen",  "Mary",  "Brown")]

        schema = StructType([StructField("dob", StringType()),
                                 StructField("gender", StringType()),
                                 StructField("salary", IntegerType()),
                                 StructField("fname", StringType()),
                                 StructField("mname", StringType()),
                                 StructField("lname", StringType()),
                                 ])
        expected_df = self.spark.createDataFrame(data, schema)
        transformed_df = renaming_nested_column(df_new)
        self.assertEqual(expected_df.collect(), transformed_df.collect())

        # testing the name whose salary is the highest one

        data = [({"firstname": "James", "middlename": "", "lastname": "Smith"}, "03011998", "M", 3000),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""}, "10111998", "M", 20000),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"}, "02012000", "M", 3000),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"}, "03011998", "F", 11000),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"}, "04101998", "F", 10000)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                             StructField("dob", StringType()),
                             StructField("gender", StringType()),
                             StructField("salary", IntegerType())])
        df = self.spark.createDataFrame(data=data, schema=schema)
        df3 = df.sort(col("salary").desc())
        df5 = df3.limit(1)
        expected_df = df5.select("name")
        transformed_df = max_salary(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())


        # testing of dropping newly added columns department and age
        data = [
                ({"firstname": "James", "middlename": "", "lastname": "Smith"},"03011998", "M", 3000,None),
                ({"firstname": "Michael", "middlename": "Rose", "lastname": ""},"10111998", "M", 20000,None),
                ({"firstname": "Robert", "middlename": "", "lastname": "Williams"},"02012000", "M", 3000,None),
                ({"firstname": "Maria", "middlename": "Anne", "lastname": "Jones"},"03011998", "F", 11000,None),
                ({"firstname": "Jen", "middlename": "Mary", "lastname": "Brown"},"04101998", "F", 10000,None)]

        schema = StructType([StructField("name", MapType(StringType(), StringType())),
                                 StructField("dob", StringType()),
                                 StructField("gender", StringType()),
                                 StructField("salary", IntegerType()),
                                 StructField("country", StringType()),
                                 ])
        expected_df = self.spark.createDataFrame(data, schema)
        transformed_df = drop_age_dept_columns(df1)
        self.assertEqual(expected_df.collect(), transformed_df.collect())


        # testing unique values of dob
        expected_df = self.spark.createDataFrame(["03011998", "10111998", "02012000", "04101998"], "string").toDF("dob")
        transformed_df = distinct_values_dob(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())

        # testing unique values of salary
        expected_df = self.spark.createDataFrame([3000, 20000, 11000, 10000], "int").toDF("dob")
        transformed_df = distinct_values_salary(df)
        self.assertEqual(expected_df.collect(), transformed_df.collect())



