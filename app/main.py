from utility import create_spark_session, read_csvs_saveto_deltalake


def main():
    spark = create_spark_session()
    read_csvs_saveto_deltalake(spark)
    spark.stop()


if __name__ == "__main__":
    main()
