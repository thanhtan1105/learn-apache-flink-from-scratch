from pyflink.common import Row
from pyflink.datastream.connectors import JdbcSink, JdbcConnectionOptions
from pyflink.common import Types, Row
import psycopg2

class PostgresUpsertSinkFunction(JdbcSink):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password

    @staticmethod
    def transform_row(row: Row) -> Row:
        return Row(
            ticker=row["ticker"],
            price=row["price"],
            volume=row["volume"],
            open_price=row["open_price"],
            high=row["high"],
            low=row["low"],
            close_price=row["close_price"],
            adjusted_close=row["adjusted_close"]
        )

    def invoke(self):
        insert_sql = """
        INSERT INTO public.stock (ticker, price, volume, open_price, high, low, close_price, adjusted_close)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (ticker)
        DO UPDATE SET price = EXCLUDED.price, volume = EXCLUDED.volume, open_price = EXCLUDED.open_price, high = EXCLUDED.high, low = EXCLUDED.low, close_price = EXCLUDED.close_price, adjusted_close = EXCLUDED.adjusted_close;
        """

        return JdbcSink.sink(
            insert_sql,
            Types.ROW([
                Types.STRING(),
                Types.DOUBLE(),
                Types.INT(),
                Types.DOUBLE(),
                Types.DOUBLE(),
                Types.DOUBLE(),
                Types.DOUBLE(),
                Types.DOUBLE()
            ]),
            JdbcConnectionOptions.JdbcConnectionOptionsBuilder()
            .with_url(self.url)
            .with_driver_name("org.postgresql.Driver")
            .with_user_name(self.username)
            .with_password(str(self.password))
            .build()
        )
