import datetime
import random
import dataclasses


@dataclasses.dataclass
class Transaction:
    account_id: int
    customer_id: str
    merchant_type: str
    transaction_id: str
    transaction_type: str
    transaction_amount: float
    transaction_date: str

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def auto(cls):
        account_id = random.randint(1000000001, 1000000010)
        customer_id = f"C{str(account_id)[::-1]}"
        merchant_type = random.choice(["Online", "In Store"])
        transaction_id = "".join(random.choice("0123456789ABCDEF") for i in range(16))
        transaction_type = random.choice(
            [
                "Grocery_Store",
                "Gas_Station",
                "Shopping_Mall",
                "City_Services",
                "HealthCare_Service",
                "Food and Beverage",
                "Others",
            ]
        )
        transaction_amount = round(random.randint(100, 10000) * random.random(), 2)
        transaction_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return cls(
            account_id,
            customer_id,
            merchant_type,
            transaction_id,
            transaction_type,
            transaction_amount,
            transaction_date,
        )

    @staticmethod
    def create(num: int):
        return [Transaction.auto() for _ in range(num)]

