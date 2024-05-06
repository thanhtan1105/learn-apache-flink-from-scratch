import datetime
import json
import random
import dataclasses


@dataclasses.dataclass
class Stock:
    event_time: str
    ticker: str
    price: float
    volume: int
    open: float
    high: float
    low: float
    close: float
    adjusted_close: float

    def __init__(self):
        self.event_time = None
        self.ticker = None
        self.price = None
        self.volume = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.adjusted_close = None

    def __init__(self, event_time: str, ticker: str, price: float, volume: int, open: float, high: float, low: float, close: float, adjusted_close: float):
        self.event_time = event_time
        self.ticker = ticker
        self.price = price
        self.volume = volume
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.adjusted_close = adjusted_close

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def auto(cls, ticker: str):
        event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        price = round(random.uniform(100, 500), 2)
        volume = random.randint(1000, 10000)
        open = round(random.uniform(100, 500), 2)
        high = round(open + random.uniform(0, 10), 2)
        low = round(open - random.uniform(0, 10), 2)
        close = round(random.uniform(low, high), 2)
        adjusted_close = round(close * random.uniform(0.95, 1.05), 2)
        return cls(event_time, ticker, price, volume, open, high, low, close, adjusted_close)

    @staticmethod
    def create():
        dict = {
            1: "AAPL",
            2: "ACN",
            3: "ADBE",
            4: "AMD",
            5: "AVGO",
            6: "CRM",
            7: "CSCO",
            8: "IBM",
            9: "INTC",
            10: "MA",
            11: "MSFT",
            12: "NVDA",
            13: "ORCL",
            14: "PYPL",
            15: "QCOM",
            16: "TXN",
            17: "V",
            18: "GOOGL",
            19: "AMZN",
            20: "FB",
            21: "NFLX",
            22: "TSLA"
        }
        tickers = list(dict.keys())
        random.shuffle(tickers)
        return [Stock.auto(dict[ticker]) for ticker in tickers]