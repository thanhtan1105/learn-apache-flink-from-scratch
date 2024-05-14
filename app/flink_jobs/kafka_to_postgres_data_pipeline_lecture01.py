from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream import CheckpointingMode, CheckpointConfig, StreamExecutionEnvironment, FileSystemCheckpointStorage
from app.utils.kafka_config import KAFKA_CONFIG
from app.utils.flink_config import FLINK_CONFIGURE
from app.utils.database_config import DATABASE_CONFIG
from app.model.stock import Stock

topic = "stock"
bootstrap_servers = KAFKA_CONFIG['bootstrap_servers']
group_id = KAFKA_CONFIG['group_id']
scan_startup_mode = KAFKA_CONFIG['scan_startup_mode']

# get the StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# configure checkpointing
(env.enable_checkpointing(FLINK_CONFIGURE['checkpoint']['interval'])
 .get_checkpoint_config()
 .set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
 .enable_unaligned_checkpoints(True)
 .set_checkpoint_timeout(FLINK_CONFIGURE['checkpoint']['timeout'])
 .set_max_concurrent_checkpoints(FLINK_CONFIGURE['checkpoint']['max_concurrent'])
 .set_checkpoint_storage(FileSystemCheckpointStorage(FLINK_CONFIGURE['checkpoint']['storage_lecture01']))
)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

(t_env.get_config()
 .get_configuration()
 .set_string("pipeline.jars", ';'.join(FLINK_CONFIGURE['pipeline']['jars']))
 )

kafka_source = """
CREATE TABLE KafkaSource (
    {}
) WITH (
    'connector' = 'kafka',
    'topic' = '{}',
    'properties.bootstrap.servers' = '{}',
    'properties.group.id' = '{}',
    'scan.startup.mode' = '{}',
    'format' = 'json'
)
""".format(Stock.asflink_structure(), topic, bootstrap_servers, group_id, scan_startup_mode)

t_env.execute_sql(kafka_source)

postgres_stock_transaction_sink = """
CREATE TABLE PostgresStockTransactionSink (
    {}
) WITH (
    'connector' = 'jdbc',
    'url' = '{}',
    'table-name' = 'public.stock_transaction',
    'username' = '{}',
    'password' = '{}',
    'driver' = 'org.postgresql.Driver'
)
""".format(Stock.aspostgres_structure(), DATABASE_CONFIG['url'], DATABASE_CONFIG['username'], DATABASE_CONFIG['password'])

t_env.execute_sql(postgres_stock_transaction_sink)

t_env.execute_sql("""
INSERT INTO PostgresStockTransactionSink
select
    CAST(event_time AS TIMESTAMP) as event_time,
    ticker,
    price,
    volume,
    open_price,
    high,
    low,
    close_price,
    adjusted_close
from KafkaSource
""").get_job_client().get_job_execution_result().result()
