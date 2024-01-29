# Use an official Python runtime as a parent image
FROM python:3.8-buster

# Install Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Expose the ports used by Spark (adjust as needed)
EXPOSE 4040 6066 7077 8080 18080
# Add the JARs to the Spark job's classpath (include all necessary JARs)
ENV SPARK_SUBMIT_ARGS="--jars /app/jars/delta-core_2.12-1.2.1.jar,/app/jars/delta-storage-1.2.1.jar,/app/jars/antlr4-runtime-4.8.jar,/app/jars/jackson-core-asl-1.9.13.jar"

# Start the Spark job
CMD ["sh", "-c", "spark-submit --master local[*] --packages io.delta:delta-core_2.12:1.2.1 --conf spark.eventLog.enabled=true --conf spark.eventLog.dir=/app/sparklogs --conf spark.history.fs.logDirectory=/app/sparklogs main.py && tail -f /dev/null"]

