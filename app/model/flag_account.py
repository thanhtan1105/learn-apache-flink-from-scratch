import datetime
import dataclasses


@dataclasses.dataclass
class FlagAccount:
    account_id: int
    flag_date: str

    def asdict(self):
        return dataclasses.asdict(self)

    @classmethod
    def auto(cls, account_id: int):
        flag_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        return cls(account_id, flag_date)

    @staticmethod
    def create():
        return [FlagAccount.auto(account_id) for account_id in range(1000000001, 1000000010, 2)]
