from Assignment_2.core_2.utils_sql_2 import *

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
        #creating a dataframe
        data = [("Banana", 1000, "USA"),

                ("Carrots", 1500, "India"),
                ("Beans", 1600, "Sweden"),
                ("Orange", 2000, "UK"),
                ("Orange", 2000, "UAE"),
                ("Banana", 400, "China"),
                ("Carrots", 1200, "China")]
        Schema = StructType([StructField("Product", StringType(), True),
                             StructField("Amount", IntegerType(), True),
                             StructField("Country", StringType(), True)])
        df = self.spark.createDataFrame(data=data, schema=Schema)

        #testinStructField("China",IntegerType(),True),g pivot operation
        data=[("Orange",None,None,None,2000,2000,None),
              ("Beans",None,None,1600,None,None,None),
              ("Banana",400,None,None,None,None,1000),
              ("Carrots",1200,1500,None,None,None,None)]
        Schema=StructType([StructField("Product",StringType(),True),
                           StructField("China",IntegerType(),True),
                           StructField("India",IntegerType(),True),
                           StructField("Sweden",IntegerType(),True),
                           StructField("UAE",IntegerType(),True),
                           StructField("UK",IntegerType(),True),
                           StructField("USA",IntegerType(),True) ])
        expected_df=self.spark.createDataFrame(data=data, schema=Schema)
        transformed_df_pivot=func_pivot(df)
        self.assertEqual(expected_df.collect(),transformed_df_pivot.collect())

        #testing unpivot
        data=[("Orange","uae",2000),
              ("Orange","uk",2000),
              ("Beans","sweden",1600),
              ("Banana","china",400),
              ("Banana","usa",1000),
              ("Carrots","china",1200),
              ("Carrots","india",1500)]
        Schema=StructType([StructField("Product",StringType(),True),
                           StructField("country",StringType(),True),
                           StructField("Total",IntegerType(),True)])
        expected_df=self.spark.createDataFrame(data=data,schema=Schema)
        transformed_df=func_unpivot(transformed_df_pivot)
        self.assertEqual(expected_df.collect(),transformed_df.collect())