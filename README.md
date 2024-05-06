# Stock Data Pipeline ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white) ![Flink](https://img.shields.io/badge/Flink-FF2E2E?style=for-the-badge&logo=apache-flink&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

This project is a data pipeline that reads stock data from a Kafka topic, processes it using Flink, and writes the results to a PostgreSQL database.

## Pre-requisites

- Docker
- Docker Compose
- Python 3.8
- Pipenv 

Run docker compose to start Kafka, Flink, and PostgreSQL services for init resource

```bash
docker-compose up -d

pip install -r requirement-dev.txt
```

## Lecture 1: Job read data from Kafka and write to PostgreSQL

### Model ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

The `Stock` class in `app/model/stock.py` represents a stock with attributes `event_time`, `ticker`, and `price`. It also includes methods to create a dictionary representation of the object and to generate random stock data.

### Kafka Configuration ![Kafka](https://img.shields.io/badge/Kafka-231F20?style=flat-square&logo=apache-kafka&logoColor=white)

The Kafka configuration in `app/utils/kafka_config.py` includes the bootstrap servers, group id, startup mode, and topic name for the Kafka consumer.

### Database Configuration ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
The Database configuration in `app/utils/db_config.py` includes the database URL, username, password, and table name for the PostgreSQL database.

### Flink Job ![Flink](https://img.shields.io/badge/Flink-FF2E2E?style=flat-square&logo=apache-flink&logoColor=white)

The Flink job in `app/flink_jobs/kafka_to_postgres_data_pipeline.py` sets up the environment, creates a Kafka source table and a PostgreSQL sink table, and executes a SQL query to transfer data from the source to the sink.

### Sample data

The sample data in `app/batch_job/app_stock_to_kafka_data_pipeline.py` includes a list of stock data with event time, ticker, and price. It will be written to the Kafka topic by the producer.

## Usage

Run the Flink job to start the data pipeline. The job will continuously read new data from the Kafka topic, process it, and write the results to the PostgreSQL database.

```bash
python -m app.batch_job.app_stock_to_kafka_data_pipeline
```

## Interfaces

- Kafka Client: http://localhost:8080/ui/clusters/local/all-topics
- PostgreSQL Admin: http://localhost:5050/browser/
