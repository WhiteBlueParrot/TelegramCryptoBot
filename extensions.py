import requests
import json

from config import currencies


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не найдена!')

        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Валюта {base} не найдена!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = float(json.loads(r.content)[currencies[base]]) * amount

        return total_base
