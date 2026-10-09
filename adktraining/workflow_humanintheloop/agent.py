# refund_agent.py

from google.adk import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext


MODEL = "gemini-3.6-flash"


# ---------------------------------------------------------
# Fake refund processing function
# ---------------------------------------------------------

def process_refund(
    amount: float,
    reason: str,
) -> dict:

    print("\nPROCESSING REFUND")
    print("Amount:", amount)
    print("Reason:", reason)

    return {
        "status": "refund processed",
        "amount": amount,
        "reason": reason,
    }


# ---------------------------------------------------------
# Human Approval Tool
# ---------------------------------------------------------

def approve_refund(
    amount: float,
    reason: str,
    tool_context: ToolContext,
) -> dict:

    """
    Refund tool that requires human approval
    for large refunds.
    """

    # -----------------------------------------------------
    # Small refunds
    # -----------------------------------------------------

    if amount <= 100:

        return process_refund(
            amount,
            reason
        )

    # -----------------------------------------------------
    # Large refund
    # Human approval required
    # -----------------------------------------------------

    confirmation = tool_context.tool_confirmation

    # First execution
    if confirmation is None:

        tool_context.request_confirmation(
            hint=(
                f"Refund request for ${amount}. "
                f"Reason: {reason}. "
                "Approve this refund?"
            ),

            payload={
                "amount": amount,
                "reason": reason,
            },
        )

        return {
            "status": "waiting for human approval"
        }

    # -----------------------------------------------------
    # Human approved
    # -----------------------------------------------------

    if confirmation.confirmed:

        return process_refund(
            amount,
            reason
        )

    # -----------------------------------------------------
    # Human rejected
    # -----------------------------------------------------

    return {
        "status": "refund rejected by human reviewer"
    }


# ---------------------------------------------------------
# Tool
# ---------------------------------------------------------

refund_tool = FunctionTool(
    func=approve_refund
)


# ---------------------------------------------------------
# Refund Agent
# ---------------------------------------------------------

root_agent = Agent(
    name="refund_agent",

    model=MODEL,

    instruction="""
You are a refund processing agent.

When the user asks for a refund:

1. Determine the refund amount.
2. Determine the reason.
3. Call approve_refund.

Rules:

Refund <= $100
    -> automatically process.

Refund > $100
    -> request human approval.

After the tool completes,
tell the user the final refund status.
""",

    tools=[
        refund_tool
    ],
)