import os
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv


class CurrencyConverterTool:
    """
    CurrencyConverterTool provides a tool function to convert an amount 
    from one currency to another using an external currency service.
    
    Attributes:
        api_key (str): The API key for the currency conversion service, 
                       loaded from environment variables.
        currency_service (CurrencyConverter): Instance of the converter service.
        currency_converter_tool_list (list): A list of registered currency converter tools.
    """

    def __init__(self):
        """
        Initialize the CurrencyConverterTool.
        - Load environment variables
        - Fetch API key for currency conversion
        - Initialize currency service
        - Register tool functions
        """
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")  # API key from .env
        self.currency_service = CurrencyConverter(self.api_key)  # Service instance
        self.currency_converter_tool_list = self._setup_tools()  # Register tool

    def _setup_tools(self) -> List:
        """
        Setup all tools for the currency converter tool.

        Returns:
            list: List of tool functions (in this case, only one: convert_currency).
        """

        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str):
            """
            Convert an amount from one currency to another.

            Args:
                amount (float): The amount of money to convert.
                from_currency (str): The currency code to convert from (e.g., "USD").
                to_currency (str): The currency code to convert to (e.g., "PKR").

            Returns:
                str: Converted amount or error message if conversion fails.
            """
            return self.currency_service.convert(amount, from_currency, to_currency)

        return [convert_currency]
