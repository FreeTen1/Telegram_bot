import requests
import json
from config import *


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Нельзя переводить одинаковые валюты {base}. Зачем???')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не получилось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не получилось обработать валюту {base}')

        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException(f'Нельзя перевести значение {amount}. Это глупо!!!')
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?base={quote_ticker}')
        total_base = float(json.loads(r.content)["rates"][base_ticker]) * amount

        return total_base


class APIException(Exception):
    pass
