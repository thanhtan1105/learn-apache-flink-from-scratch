import datetime
import json
import random
import dataclasses


@dataclasses.dataclass
class Stock:
    event_time: str
    ticker: str
    price: float

    def __init__(self):
        self.event_time = None
        self.ticker = None
        self.price = None

    def __init__(self, event_time: str, ticker: str, price: float):
        self.event_time = event_time
        self.ticker = ticker
        self.price = price

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def auto(cls, ticker: str):
        # event_time = datetime.datetime.now().isoformat(timespec="milliseconds")
        event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        price = round(random.random() * 100, 2)
        return cls(event_time, ticker, price)

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
            17: "V"
        }
        tickers = list(dict.keys())
        random.shuffle(tickers)
        print(tickers)
        return [Stock.auto(dict[ticker]) for ticker in tickers]
