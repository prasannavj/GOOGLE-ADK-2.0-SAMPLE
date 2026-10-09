# agent.py

from typing import Literal

from pydantic import BaseModel

from google.adk import Agent, Workflow


MODEL = "gemini-3.6-flash"


# ---------------------------------------------------------
# 1. STRUCTURED ROUTER OUTPUT
# ---------------------------------------------------------

class SupportRoute(BaseModel):
    route: Literal[
        "billing",
        "technical",
        "general",
    ]


# ---------------------------------------------------------
# 2. ROUTER AGENT
# ---------------------------------------------------------

router_agent = Agent(
    name="router_agent",

    model=MODEL,

    instruction="""
You are a support request classifier.

Classify the customer's request into exactly one category:

billing
technical
general

Examples:

"My invoice is wrong"
-> billing

"My application is not starting"
-> technical

"What are your support hours?"
-> general
""",

    output_schema=SupportRoute,
)


# ---------------------------------------------------------
# 3. SPECIALIST AGENTS
# ---------------------------------------------------------

billing_agent = Agent(
    name="billing_agent",
    model=MODEL,

    instruction="""
You are a billing specialist.

Handle:
- invoice questions
- payment problems
- refunds
- subscriptions
- charges

Provide concise and helpful answers.
""",
)


technical_agent = Agent(
    name="technical_agent",
    model=MODEL,

    instruction="""
You are a technical support specialist.

Handle:
- application errors
- login problems
- installation issues
- system failures
- technical troubleshooting

Provide step-by-step troubleshooting.
""",
)


general_agent = Agent(
    name="general_agent",
    model=MODEL,

    instruction="""
You handle general customer support questions.

Answer clearly and professionally.
""",
)