import pytest
from unittest.mock import patch
from utility import (create_spark_session,
                     read_csvs_saveto_deltalake,
                     internet_on,
                     logger)
from pyspark.sql import SparkSession
import json


# Fixture for Spark Session
@pytest.fixture(scope="module")
def spark():
    spark = SparkSession.builder \
        .appName("TestApp") \
        .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1") \
        .config("spark.network.timeout", "600s") \
        .config("spark.sql.extensions",
                "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog",
                "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
        .getOrCreate()
    yield spark
    spark.stop()


# Fixture for loading configuration
@pytest.fixture(scope="module")
def config():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config


# Test internet_on function
@patch('socket.socket')
def test_internet_on(mock_socket):
    mock_socket.return_value.connect.return_value = True
    assert internet_on(logger) == True


# Test create_spark_session function
@patch('utility.internet_on')
def test_create_spark_session(mock_internet_on):
    mock_internet_on.return_value = True
    spark = create_spark_session()
    assert spark is not None
    assert isinstance(spark, SparkSession)


# Test read_csvs_saveto_deltalake function
def test_read_csvs_saveto_deltalake(spark, tmpdir):
    # Create a temporary directory and a dummy CSV file
    input_dir = tmpdir.mkdir("input_test")
    output_dir = tmpdir.mkdir("output_test")
    dummy_csv = input_dir.join("dummy.csv")
    dummy_csv.write("a,b,c\nd,e,f")

    # Define paths
    input_path = str(input_dir)
    output_path = str(output_dir)
    # Run the function
    df = read_csvs_saveto_deltalake(spark,
                                    input=input_path,
                                    output=output_path,
                                    header=True,
                                    sep=","
                                    )
    # Check if the function returns a DataFrame
    assert df is not None
    # Check if the DataFrame has the correct number of rows
    assert df.count() == 1
    # Check if the DataFrame has the correct number of columns
    assert len(df.columns) == 5
