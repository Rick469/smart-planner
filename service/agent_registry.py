from agents.intent_agent import IntentAgent
from agents.planner_agent import PlannerAgent
from agents.attraction_agent import AttractionAgent
from agents.hotel_agent import HotelAgent
from agents.weather_agent import WeatherAgent


class AgentRegistry:


    def __init__(self, checkpointer):


        self.intent_agent = IntentAgent(
            stream=True,
            checkpointer=checkpointer
        )


        self.planner_agent = PlannerAgent(
            stream=True,
            checkpointer=checkpointer
        )


        self.attraction_agent = AttractionAgent(
            stream=True
        )


        self.hotel_agent = HotelAgent(
            stream=True
        )


        self.weather_agent = WeatherAgent(
            stream=True
        )