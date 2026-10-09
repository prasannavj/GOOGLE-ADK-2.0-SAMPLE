# collaborative_agent.py

from google.adk import Agent


MODEL = "gemini-3.6-flash"


# ---------------------------------------------------------
# Flight Agent
# ---------------------------------------------------------

flight_agent = Agent(
    name="flight_agent",

    mode="single_turn",

    description="""
Use this agent when flight recommendations are required.
""",

    instruction="""
You are a flight specialist.

Based on the user's travel request:

1. Identify origin.
2. Identify destination.
3. Identify travel dates if available.
4. Suggest reasonable flight options.

This is a demonstration application.

Do not claim live availability.
Give simple example flight recommendations.
""",
)


# ---------------------------------------------------------
# Hotel Agent
# ---------------------------------------------------------

hotel_agent = Agent(
    name="hotel_agent",

    mode="single_turn",

    description="""
Use this agent when hotel recommendations are required.
""",

    instruction="""
You are a hotel specialist.

Based on the user's destination:

1. Recommend 2 or 3 hotels.
2. Mention approximate category.
3. Mention suitable area.
4. Explain briefly why each hotel is suitable.

Do not claim live availability.
""",
)


# ---------------------------------------------------------
# Activity Agent
# ---------------------------------------------------------

activity_agent = Agent(
    name="activity_agent",

    mode="single_turn",

    description="""
Use this agent when sightseeing or activities are required.
""",

    instruction="""
You are a tourism specialist.

Recommend:

- tourist attractions
- activities
- places to visit

Keep the recommendations simple.
""",
)


# ---------------------------------------------------------
# Coordinator
# ---------------------------------------------------------

root_agent = Agent(
    name="travel_coordinator",

    model=MODEL,

    instruction="""
You are a travel planning coordinator.

Use your specialist agents when appropriate.

flight_agent
    -> flight recommendations

hotel_agent
    -> hotel recommendations

activity_agent
    -> attractions and activities

For a full trip request:

1. Ask flight_agent for flight recommendations.
2. Ask hotel_agent for hotel recommendations.
3. Ask activity_agent for activities.
4. Combine the results into one simple travel plan.

Present the final answer under:

Flights
Hotels
Activities
Suggested itinerary
""",

    sub_agents=[
        flight_agent,
        hotel_agent,
        activity_agent,
    ],
)