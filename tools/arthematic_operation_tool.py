import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

load_dotenv()


@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b


@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b


@tool
def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """
    Convert an amount from one currency to another using Alpha Vantage API.

    Args:
        from_curr (str): The currency code to convert from (e.g., "USD").
        to_curr (str): The currency code to convert to (e.g., "PKR").
        value (float): The amount to convert.

    Returns:
        float: The converted amount in the target currency.
    """
    # Ensure the API key is available
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise ValueError("Missing ALPHAVANTAGE_API_KEY in environment variables.")

    # Set environment variable so AlphaVantageAPIWrapper can pick it up
    os.environ["ALPHAVANTAGE_API_KEY"] = api_key

    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)

    # Defensive: make sure response has the expected structure
    try:
        exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']

    except (KeyError, TypeError):
        raise ValueError(f"Unexpected response format: {response}")

    return round(value * float(exchange_rate), 2)  # rounded for clarity
