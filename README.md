# home_task2_nidhal
## Overview
This project is about reading a cvs file or multi csv files with or without header

## Configuration
The project uses a `config.json` file for configuration. Here's what each property does:

- `paths`: This object contains paths to various resources used by the project.
  - `input_csv`: The path to the input CSV file.
  - `output_deltalake`: The path where the output Delta Lake will be stored.
  - `job_local_logs`: The path where local logs for the job will be stored.
  - `delta_jar_file`: The path to the Delta Lake JAR file in case no internet.
  - `dependencies`: The paths to the dependency JAR files, separated by commas.

- `variables`: This object contains various settings for the project.
  - `app_name`: The name of the application.
  - `header`: Whether the CSV file has a header row. Should be either "True" or "False".
  - `sep`: The character used to separate fields in the CSV file.

## How to Run
dockerfile and yaml file provided to compose and run the job:
	-when inside the project folder run: docker-compose up
	
use the spark-submit to run the main.py file
