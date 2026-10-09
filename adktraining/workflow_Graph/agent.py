# graph_agent.py

from typing import Literal

from pydantic import BaseModel

from google.adk import Agent, Context, Event, Workflow
from google.adk.workflow import node, START


MODEL = "gemini-3.6-flash"


# ---------------------------------------------------------
# Structured output
# ---------------------------------------------------------

class RouteResult(BaseModel):
    route: Literal[
        "billing",
        "technical",
        "general",
    ]


# ---------------------------------------------------------
# Router Agent
# ---------------------------------------------------------

router_agent = Agent(
    name="router_agent",
    model=MODEL,

    instruction="""
You are a customer support router.

Classify the user's request into exactly one category:

billing
technical
general

Examples:

"I was charged twice"
-> billing

"I cannot login"
-> technical

"What are your working hours?"
-> general
""",

    output_schema=RouteResult,
)


# ---------------------------------------------------------
# Billing Agent
# ---------------------------------------------------------

billing_agent = Agent(
    name="billing_agent",
    model=MODEL,

    instruction="""
You are a billing support specialist.

Handle:
- payments
- invoices
- refunds
- duplicate charges
- subscriptions

Give a short and helpful answer.
""",
)


# ---------------------------------------------------------
# Technical Agent
# ---------------------------------------------------------

technical_agent = Agent(
    name="technical_agent",
    model=MODEL,

    instruction="""
You are a technical support specialist.

Handle:
- login problems
- application errors
- installation issues
- technical troubleshooting

Give simple step-by-step guidance.
""",
)


# ---------------------------------------------------------
# General Agent
# ---------------------------------------------------------

general_agent = Agent(
    name="general_agent",
    model=MODEL,

    instruction="""
You handle general customer support questions.

Answer clearly and briefly.
""",
)


# ---------------------------------------------------------
# Dynamic Router Node
#
# IMPORTANT:
# rerun_on_resume=True is mandatory because this
# function calls ctx.run_node()
# ---------------------------------------------------------

@node(rerun_on_resume=True)
async def route_request(
    ctx: Context,
    node_input: str,
):

    # -----------------------------------------------------
    # Step 1: Ask router agent to classify the request
    # -----------------------------------------------------

    result = await ctx.run_node(
        router_agent,
        node_input=node_input,
    )

    print("Router Result:", result)

    # Depending on ADK/Pydantic serialization,
    # result may be a model or dictionary.

    if isinstance(result, dict):
        route = result["route"]
    else:
        route = result.route

    print("Selected Route:", route)

    # -----------------------------------------------------
    # Step 2: Dynamic routing
    # -----------------------------------------------------

    if route == "billing":

        response = await ctx.run_node(
            billing_agent,
            node_input=node_input,
        )

    elif route == "technical":

        response = await ctx.run_node(
            technical_agent,
            node_input=node_input,
        )

    else:

        response = await ctx.run_node(
            general_agent,
            node_input=node_input,
        )

    # -----------------------------------------------------
    # Step 3: Return workflow output
    #
    # Dynamic workflow parent is an async generator.
    # Yield Event instead of return response.
    # -----------------------------------------------------

    yield Event(
        output=response
    )


# ---------------------------------------------------------
# Workflow
# ---------------------------------------------------------

root_agent = Workflow(
    name="support_workflow",

    edges=[
        (
            START,
            route_request,
        )
    ],
)