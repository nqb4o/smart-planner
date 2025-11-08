from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool


class CalculatorTool:
    """
    CalculatorTool provides LangChain-compatible tools for handling common
    travel and expense-related calculations (hotel cost, total trip expense,
    and daily budget).
    """

    def __init__(self):
        """Initialize the CalculatorTool with an instance of Calculator."""
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """
        Setup all tools for the calculator tool.

        Returns:
            list: List of registered calculator tool functions.
        """

        @tool
        def estimate_total_hotel_cost(price_per_night: float, total_days: float) -> float:
            """
            Calculate total hotel cost.

            Args:
                price_per_night (float): Cost per night at the hotel.
                total_days (float): Number of nights.

            Returns:
                float: Total hotel cost.
            """
            return self.calculator.multiply(price_per_night, total_days)

        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """
            Calculate total expense of the trip by summing a list of costs.

            Args:
                costs (List[float]): A list of numerical expense values.

            Returns:
                float: Sum of all provided costs.
            """
            # The 'costs' variable is now a list, e.g., [100, 50, 20]
            # We pass its elements to the calculator function using the * operator to unpack them.
            return self.calculator.calculate_total(*costs)

        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """
            Calculate daily expense budget.

            Args:
                total_cost (float): Total cost of the trip.
                days (int): Number of days of the trip.

            Returns:
                float: Daily budget.
            """
            return self.calculator.calculate_daily_budget(total_cost, days)

        return [
            estimate_total_hotel_cost,
            calculate_total_expense,
            calculate_daily_expense_budget
        ]