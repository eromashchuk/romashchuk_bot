import requests
import json
from config import keys

class APIException(BaseException):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, qty: float):
        try:
            base_t = keys[base]
        except KeyError:
            raise APIException(f"Нет данных для {base} валюты")
        try:
            quote_t = keys[quote]
        except KeyError:
            raise APIException(f"Нет данных для {quote} валюты")
        try:
            qty = float(qty)
        except ValueError:
            raise APIException("Введите сумму числом, можно с плавающей точкой")
        else:
            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_t}&tsyms={quote_t}')
            total_base = json.loads(r.content)[quote_t] * qty
            return total_base

