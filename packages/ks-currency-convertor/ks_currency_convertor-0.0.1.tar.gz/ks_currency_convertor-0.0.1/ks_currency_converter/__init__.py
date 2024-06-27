import requests

class CurrencyConverter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"

    def get_exchange_rate(self, from_currency, to_currency):
        response = requests.get(self.url + from_currency)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Error fetching exchange rate data: {data['error-type']}")

        rates = data["conversion_rates"]
        if to_currency not in rates:
            raise ValueError(f"Currency {to_currency} not found in exchange rates.")
        
        return rates[to_currency]

    def convert(self, amount, from_currency, to_currency):
        rate = self.get_exchange_rate(from_currency, to_currency)
        return amount * rate


# converter = CurrencyConverter("5ea8fd42252121cf83a4738d")

# # Get the conversion rate from USD to EUR
# usd_to_eur_rate = converter.get_exchange_rate("USD", "EUR")
# print(f"1 USD is equal to {usd_to_eur_rate} EUR")
   
