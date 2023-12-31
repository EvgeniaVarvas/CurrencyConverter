from keysconfig import keys
import requests
import json

class ConversionException(Exception):
    pass

class СurrencyСonverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        
        if quote == base:
            raise ConversionException(f'Невозможно перевести одинаковые валюты {base}.')
    
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {quote}.')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {base}.')    
        
        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество {amount}.')
        res = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')

    
        total_base = json.loads(res.content)[keys[base]]
        return total_base