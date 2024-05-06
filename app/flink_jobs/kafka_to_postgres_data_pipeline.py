from pyflink.table import StreamTableEnvironment, EnvironmentSettings
# from app.utils.kafka_config import KAFKA_CONFIG
from ..utils.kafka_config import KAFKA_CONFIG

topic = "stock"
bootstrap_servers = KAFKA_CONFIG['bootstrap_servers']
group_id = "stock_group"
scan_startup_mode = KAFKA_CONFIG['scan_startup_mode']

settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
t_env = StreamTableEnvironment.create(environment_settings=settings)

(t_env.get_config()
 .get_configuration()
 .set_string("pipeline.jars", "file:///Users/lethanhtan/PycharmProjects/flink_kafka_to_kafka/packages/lib/flink-connector-kafka_2.12-1.14.6.jar;"
             + "file:///Users/lethanhtan/PycharmProjects/flink_kafka_to_kafka/packages/lib/kafka-clients-2.4.1.jar;"
             + "file:///Users/lethanhtan/PycharmProjects/flink_kafka_to_kafka/packages/lib/postgresql-42.6.2.jar;"
             + "file:///Users/lethanhtan/PycharmProjects/flink_kafka_to_kafka/packages/lib/flink-connector-jdbc_2.12-1.14.0.jar"
               ))

kafka_source = """
CREATE TABLE KafkaSource (
    event_time STRING,
    ticker STRING,
    price DOUBLE
) WITH (
    'connector' = 'kafka',
    'topic' = '{}',
    'properties.bootstrap.servers' = '{}',
    'properties.group.id' = '{}',
    'scan.startup.mode' = '{}',
    'format' = 'json'
)
""".format(topic, bootstrap_servers, group_id, scan_startup_mode)

t_env.execute_sql(kafka_source)

postgres_sink = """
CREATE TABLE PostgresSink (
    event_time Timestamp,
    ticker STRING,
    price DOUBLE
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://localhost:5432/finance_advise',
    'table-name' = 'stock',
    'username' = 'admin',
    'password' = '123456',
    'driver' = 'org.postgresql.Driver'
)
"""

t_env.execute_sql(postgres_sink)

result = t_env.execute_sql("""
INSERT INTO PostgresSink
select
    CAST(event_time AS TIMESTAMP) as event_time,
    ticker,
    price
from KafkaSource
""")

result.get_job_client().get_job_execution_result().result()
