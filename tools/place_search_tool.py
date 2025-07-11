from utils.place_info_search import TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place:str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = self.tavily_search.tavily_search_attractions(place)
                return f"Following are the attractions of {place}: {attraction_result}"
            except Exception as e:
                return f"Error searching for attractions in {place}: {str(e)}"
        
        @tool
        def search_restaurants(place:str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Following are the restaurants of {place}: {restaurants_result}"
            except Exception as e:
                return f"Error searching for restaurants in {place}: {str(e)}"
        
        @tool
        def search_activities(place:str) -> str:
            """Search activities of a place"""
            try:
                activities_result = self.tavily_search.tavily_search_activity(place)
                return f"Following are the activities in and around {place}: {activities_result}"
            except Exception as e:
                return f"Error searching for activities in {place}: {str(e)}"
        
        @tool
        def search_transportation(place:str) -> str:
            """Search transportation of a place"""
            try:
                transportation_result = self.tavily_search.tavily_search_transportation(place)
                return f"Following are the modes of transportation available in {place}: {transportation_result}"
            except Exception as e:
                return f"Error searching for transportation in {place}: {str(e)}"
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]