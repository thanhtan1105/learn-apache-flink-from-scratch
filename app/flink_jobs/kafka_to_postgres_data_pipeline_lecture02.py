from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream import CheckpointingMode, CheckpointConfig, StreamExecutionEnvironment, FileSystemCheckpointStorage
from app.utils.kafka_config import KAFKA_CONFIG
from app.utils.flink_config import FLINK_CONFIGURE
from app.utils.database_config import DATABASE_CONFIG
from pyflink.common import Types, Row
from pyflink.common.typeinfo import RowTypeInfo
from app.model.stock import Stock
from app.functions.flink_function import PostgresUpsertSinkFunction

# get the StreamExecutionEnvironment
env = StreamExecutionEnvironment.get_execution_environment()

# configure checkpointing
(env.enable_checkpointing(FLINK_CONFIGURE['checkpoint']['interval'])
 .get_checkpoint_config()
 .set_checkpointing_mode(CheckpointingMode.EXACTLY_ONCE)
 .enable_unaligned_checkpoints(True)
 .set_checkpoint_timeout(FLINK_CONFIGURE['checkpoint']['timeout'])
 .set_max_concurrent_checkpoints(FLINK_CONFIGURE['checkpoint']['max_concurrent'])
 .set_checkpoint_storage(FileSystemCheckpointStorage(FLINK_CONFIGURE['checkpoint']['storage_lecture02']))
)

t_env = StreamTableEnvironment.create(env, environment_settings=EnvironmentSettings.new_instance().in_streaming_mode().build())

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
""".format(Stock.asflink_structure(), 'stock', KAFKA_CONFIG['bootstrap_servers'], KAFKA_CONFIG['group_id'], KAFKA_CONFIG['scan_startup_mode'])

t_env.execute_sql(kafka_source)

kafka_source_stream = t_env.to_append_stream(
    t_env.sql_query("SELECT ticker, price, volume, open_price, high, low, close_price, adjusted_close FROM KafkaSource"),
    RowTypeInfo(
        [Types.STRING(), Types.DOUBLE(), Types.INT(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE()],
        ["ticker", "price", "volume", "open_price", "high", "low", "close_price", "adjusted_close"]
    )
)

kafka_source_stream = kafka_source_stream.map(lambda row: PostgresUpsertSinkFunction.transform_row(row), RowTypeInfo(
        [Types.STRING(), Types.DOUBLE(), Types.INT(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE(), Types.DOUBLE()],
        ["ticker", "price", "volume", "open_price", "high", "low", "close_price", "adjusted_close"]
    ))

kafka_source_stream.add_sink(PostgresUpsertSinkFunction(DATABASE_CONFIG['url'], DATABASE_CONFIG['username'], DATABASE_CONFIG['password']).invoke())
env.execute("Kafka to Postgres Data Pipeline Lecture 02")
