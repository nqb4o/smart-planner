import requests


class CurrencyConverter:
    def __init__(self, api_key: str):
        """
        Initialize the CurrencyConverter with API key.
        Args:
            api_key (str): Your ExchangeRate API key.
        """
        # Base URL for ExchangeRate API (latest exchange rates by base currency)
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest"

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert the amount from one currency to another.
        
        Args:
            amount (float): Amount to convert.
            from_currency (str): Source currency code (e.g., "USD").
            to_currency (str): Target currency code (e.g., "PKR").
        
        Returns:
            float: Converted amount in target currency.
        
        Raises:
            Exception: If API call fails.
            ValueError: If the target currency is not found.
        """
        # API endpoint for base currency
        url = f"{self.base_url}/{from_currency.upper()}"
        response = requests.get(url)

        if response.status_code != 200:
            # Safer to return JSON only if it's valid, else str
            try:
                error_message = response.json()
            except Exception:
                error_message = response.text
            raise Exception(f"API call failed: {error_message}")

        data = response.json()
        rates = data.get("conversion_rates", {})

        if to_currency.upper() not in rates:
            raise ValueError(f"{to_currency.upper()} not found in exchange rates.")

        return round(amount * rates[to_currency.upper()], 2)  # Rounded for user-friendliness
