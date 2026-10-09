from google.adk.events import Event
from google.adk import Workflow
from google.adk import Agent
from pydantic import BaseModel

class PlayerTypeModel(BaseModel):
    name: str
    player_type: str
    name: str

class BowlerTypeModel(BaseModel):
    name: str
    wickets: int

class BatterTypeModel(BaseModel):
    name: str
    runs: int

player_type_agent = Agent(
    name="player_type_agent",
    model="gemini-flash-lite-latest",
    output_schema=PlayerTypeModel,
    instruction="""
       Find if given player is a bowler first or batter first in test match.
       If it is bowler, set player_type to bowler.
       If it is batter, set player_type to batter.
       If player does not exist or has not played any test match, set player_type to na. 
    """,
)
bowler_stats_agent = Agent(
    name="bowler_stats_agent",
    model="gemini-flash-lite-latest",
    input_schema=PlayerTypeModel,
    output_schema=BowlerTypeModel,
    instruction="""
      Find total number of wickets taken by  {PlayerTypeModel.name} in test matches. 
    """,
)
batter_stats_agent = Agent(
    name="batter_stats_agent",
    model="gemini-flash-lite-latest",
    input_schema=PlayerTypeModel,
    output_schema=BowlerTypeModel,
    instruction="""
      Find total number of runs scored  by  {PlayerTypeModel.name} in test matches. 
    """,
)

def no_record_available(node_input: PlayerTypeModel):
    print(f"No record exist for {node_input.name}!!!!")


def player_router(node_input: PlayerTypeModel):
    """Route to task B or C based on node_input."""
    if node_input.player_type == "batter":
        return Event(route="BATTER_ROUTE")  
    if node_input.player_type == "bowler":
        return Event(route="BOWLER_ROUTE")  
    if node_input.player_type == "na":
        return Event(route="NA_ROUTE")  

root_agent = Workflow(
    name="root_agent",
    edges=[
        ("START", player_type_agent, player_router),
        (
            player_router,
            {
                "BOWLER_ROUTE": bowler_stats_agent,
                "BATTER_ROUTE": batter_stats_agent,
                "NA_ROUTE": no_record_available,
            },
        ),
    ],
)
