# CurrencyConverter - Python Package for Exchange Rates

This Python package provides a `CurrencyConverter` class to retrieve exchange rates and convert amounts between different currencies.

## Features:

- Fetches live exchange rates from a reputable API.
- Converts currency amounts based on retrieved rates.
- Handles errors for invalid API responses and missing currencies.

## Installation:

Install the package using pip:

```bash
pip install ks-currency-converter
```
## Usage:

Import the CurrencyConverter class:

```bash
import ks_currency_converter
```

## Create an instance of CurrencyConverter with your API key (replace with your own):
```bash
converter = ks_currency_converter.CurrencyConverter("YOUR_API_KEY")
```

Obtain a free API key from the currency exchange API provider {ExchangeRate-API}.

## Get the exchange rate for a specific currency pair:
```bash
usd_to_eur_rate = converter.get_exchange_rate("USD", "EUR")
print(f"1 USD is equal to {usd_to_eur_rate} EUR")
```
## Convert an amount between currencies:
```bash
amount_to_convert = 100
converted_amount = converter.convert(amount_to_convert, "USD", "JPY")
print(f"{amount_to_convert} USD is equal to {converted_amount} JPY")
```

## API Key:
You need a valid API key from a currency exchange API provider to use this package. The provided example key (5ea8fd42252121cf83a4738d) is for demonstration purposes only and may not be functional.

## Development and Testing:
This package offers basic functionality and error handling. Consider these points for further development:

## Implement caching for retrieved exchange rates.
Add unit tests to ensure code functionality.
## Contributing:
We welcome contributions to improve this package. Feel free to submit pull requests with enhancements or bug fixes.