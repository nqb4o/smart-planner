from langchain_tavily import TavilySearch


class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    @staticmethod
    def tavily_search_attractions(place: str) -> dict:
        """Searches for attractions in the specified place using TavilySearch."""

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        print(result)
        return result.get("answer") if isinstance(result, dict) and result.get("answer") else result

    @staticmethod
    def tavily_search_restaurants(place: str) -> dict:
        """Searches for available restaurants in the specified place using TavilySearch."""

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        print(result)
        return result.get("answer") if isinstance(result, dict) and result.get("answer") else result

    @staticmethod
    def tavily_search_activity(place: str) -> dict:
        """Searches for popular activities in the specified place using TavilySearch."""

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activties in and around {place}"})
        print(result)
        return result.get("answer") if isinstance(result, dict) and result.get("answer") else result

    @staticmethod
    def tavily_search_transportation(place: str) -> dict:
        """Searches for available modes of transportation in the specified place using TavilySearch."""

        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        print(result)
        return result.get("answer") if isinstance(result, dict) and result.get("answer") else result
