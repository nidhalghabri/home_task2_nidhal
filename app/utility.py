import logging
from logging.handlers import RotatingFileHandler
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
import uuid
import os
import socket
from pyspark.sql.functions import date_format
import json


with open('config.json', 'r') as config_file:
    config = json.load(config_file)


# ######################### logger #########################
def logger():
    # Specify your log directory path here
    log_dir = config['paths']['job_local_logs']
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    # Specify your log file name here
    log_file = os.path.join(log_dir, 'logfile.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(log_file, maxBytes=10485760, backupCount=5),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


# Set up logging directory and file
logger = logger()


# ######################### create_spark_session #########################
# test if internet is available
def internet_on(host="8.8.8.8", port=53, timeout=3):
    try:
        # Create a socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.close()  # Close the socket after the check
        return True
    except socket.error as ex:
        logger.error(f"Internet check failed: {ex}")
        return False


# based on internet availability, create spark session
def create_spark_session():
    logger.info(f"Creating Spark session: {config['variables']['app_name']}")
    if internet_on():
        logger.info("Internet is available, downloading Delta Lake package.")
        spark = SparkSession.builder \
            .appName(config['variables']['app_name']) \
            .config("spark.jars.packages", "io.delta:delta-core_2.12:1.2.1") \
            .config("spark.sql.extensions",
                    "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog",
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
            .getOrCreate()
    else:
        delta_jar_file = config['paths']['delta_jar_file']
        dep = config['paths']['dependencies']
        logger.info("Internet is not available, using local Delta Lake JAR.")
        spark = SparkSession.builder \
            .appName(config['variables']['app_name']) \
            .config("spark.jars", delta_jar_file+','+dep) \
            .config("spark.sql.extensions",
                    "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog",
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
            .getOrCreate()
    return spark
# #########################################################################


# read_csvs_saveto_deltalake
def read_csvs_saveto_deltalake(spark,
                               input=config['paths']['input_csv'],
                               output=config['paths']['output_deltalake'],
                               header=config['variables']['header'],
                               sep=config['variables']['sep'],):
    logger.info(f"""
                Reading CSV files from {input}
                and saving to Delta Lake at
                {output}""")
    file_pattern = f"{input}/*.csv"
    os.makedirs(output, exist_ok=True)
    df = spark.read.csv(
        file_pattern,
        header=header,
        sep=sep,
        inferSchema=True)
    df = df.withColumn("ingestion_tms", date_format(current_timestamp(),
                                                    "yyyy-MM-dd HH:mm:ss")) \
           .withColumn("batch_id", lit(str(uuid.uuid4())))
    df.write.format("delta").mode("append")\
        .save(config['paths']['output_deltalake'])
    logger.info("Data saved to Delta Lake successfully.")
    return df
