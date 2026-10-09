#from google.adk.agents.llm_agent import Agent


#Example-1 - simple agent

# root_agent = Agent(
#     model='gemini-3.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )



#Example-2 - agent with tools

# import random


# # 1. Define a simple native Python tool
# def get_flight_status(flight_number: str) -> str:
#     """
#     Retrieves the current status of a flight.
    
#     Args:
#         flight_number: The alphanumeric flight code (e.g., 'AA123', 'DL456').
#     """
#     statuses = ["On Time", "Delayed by 45 minutes", "Boarding", "Cancelled"]
#     selected_status = random.choice(statuses)
#     return f"Flight {flight_number} is currently: {selected_status}."

# # 2. Define the core instructions for the agent
# agent_instruction = """
# You are a helpful travel assistant. Whenever a user asks about a flight's status, 
# always use the provided `get_flight_status` tool to fetch real-time information. 
# Do not guess or simulate flight metrics yourself.
# """

# # 3. Create the root agent and pass the tool function directly into the list
# root_agent = Agent(
#     model="gemini-3.6-flash",  # Or "gemini-3.5-flash" depending on your framework version
#     name="travel_status_assistant",
#     instruction=agent_instruction,
#     tools=[get_flight_status],  # ADK automatically converts this native function into a tool
# )


#Example-3 - agent with sub agent

# # --- Define Tools for Sub-Agents ---
# def get_weather(city: str) -> dict:
#     """Return the current weather report for a given city."""
#     # In a real app, you would fetch from a weather API here
#     return {"status": "success", "report": f"It's 22°C and sunny in {city}."}

# def search_flights(destination: str) -> dict:
#     """Search for available flights to a specific destination."""
#     return {"status": "success", "flights": f"Found 3 direct flights to {destination} starting at $350."}

# # --- Create Specialized Sub-Agents ---
# # Note: The description tells the parent agent when to route work here.
# weather_agent = Agent(
#     name="weather_checker",
#     model="gemini-3.6-flash",
#     description="Useful for checking weather forecasts and current conditions in a city.",
#     instruction="You are a weather specialist. Use the get_weather tool to look up information.",
#     tools=[get_weather],
#     mode="single_turn" # Executed without waiting for extra user input
# )

# flight_agent = Agent(
#     name="flight_booker",
#     model="gemini-3.6-flash",
#     description="Useful for finding, searching, or booking flights to a destination.",
#     instruction="You are a flight booking assistant. Use search_flights to assist the user.",
#     tools=[search_flights],
#     mode="task"
# )

# # --- Create Root Coordinator Agent ---
# # Simply passing sub_agents automatically auto-injects delegation tools
# root_agent = Agent(
#     name="travel_planner",
#     model="gemini-3.6-flash",
#     instruction=(
#         "You are a master travel planner. Greet the user, understand their request, "
#         "and delegate to your sub-agents (weather_checker or flight_booker) as needed "
#         "to answer their questions comprehensively."
#     ),
#     sub_agents=[weather_agent, flight_agent] 
# )


#Example-4 - ADK 2.0  - workflow - Linear workflow


from google.adk.events import Event
from google.adk import Workflow # type: ignore
from google.adk import Agent
from pydantic import BaseModel
'''
Twitter Post Generator
1. User enters a Topic, thus triggering Workflow execution
2. This Topic is supplied to top_keyword_finder_agent as String
3. The output of this node is KeywordTopicModel containing keyword, supplied as input to next node twitter_agent
4. The output of twitter_agent node is TwitterPostModel containing {topic,keyword,post}. Finally we may use `post` as output
'''
class KeywordTopicModel(BaseModel):
    keyword: str
    topic:str 
class TwitterPostModel(BaseModel):
    topic: str
    keyword: str
    post: str

top_keyword_finder_agent = Agent(
    name="top_keyword_finder_agent",
    model="gemini-flash-lite-latest",
    output_schema=KeywordTopicModel,
    instruction="""Find single topmost ranking keyword for topic supplied by user."""
)
twitter_agent = Agent(
    name="twitter_agent",
    model="gemini-flash-lite-latest",
    input_schema=KeywordTopicModel,
    output_schema=TwitterPostModel,
    instruction="""Write a twitter post for {KeywordTopicModel.keyword}.""",
)
root_agent = Workflow(
    name="root_agent",
    edges=[("START", top_keyword_finder_agent, twitter_agent)],
)
