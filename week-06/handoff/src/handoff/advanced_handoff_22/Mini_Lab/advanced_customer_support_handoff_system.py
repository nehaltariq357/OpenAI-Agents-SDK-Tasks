import os
from agents import Agent, Runner, handoff, RunContextWrapper,function_tool,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel
from agents.extensions import handoff_filters
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client

)

# --- Define the data for our "briefing note" ---
class HandoffData(BaseModel):
    summary: str

# --- Define our specialist agents ---
billing_agent = Agent(name="Billing Agent", instructions="Handle billing questions.",model=model)
technical_agent = Agent(name="Technical Support Agent", instructions="Troubleshoot technical issues.",model=model)

# --- Define our on_handoff callback ---
def log_the_handoff(ctx: RunContextWrapper, input_data: HandoffData):
    print(f"\n[SYSTEM: Handoff initiated. Briefing: '{input_data.summary}']\n")

# --- TODO 1: Create the advanced handoffs ---

# Create a handoff to `billing_agent`.
# - Override the tool name to be "transfer_to_billing".
# - Use the `log_the_handoff` callback.
# - Require `HandoffData` as input.
to_billing_handoff = handoff(
    agent=billing_agent,
    tool_name_override="transfer_to_billing",
    input_type=HandoffData,
    on_handoff=log_the_handoff,
    # Your code here
)

# Create a handoff to `technical_agent`.
# - Use the `log_the_handoff` callback.
# - Require `HandoffData` as input.
# - Add an input filter: `handoff_filters.remove_all_tools`.
to_technical_handoff = handoff(
    agent=technical_agent,
    input_type=HandoffData,
    on_handoff=log_the_handoff,
    input_filter=handoff_filters.remove_all_tools
    # Your code here
)
@function_tool
def diagnose() -> str:
    """Fake diagnostic tool — always says payment failed"""
    return "The user's payment failed."

# --- Triage Agent uses the handoffs ---
triage_agent = Agent(
    name="Triage Agent",
    instructions="First, use the 'diagnose' tool. Then, based on the issue, handoff to the correct specialist with a summary.",
    tools=[diagnose],
    handoffs=[to_billing_handoff, to_technical_handoff],
    model=model
)

def main():
    print("--- Running Scenario: Billing Issue ---")
    result =  Runner.run_sync(triage_agent, "My payment won't go through.")
    print(f"Final Reply From: {result.last_agent.name}")
    print(f"Final Message: {result.final_output}")

    
# output:
# --- Running Scenario: Billing Issue ---

# [SYSTEM: Handoff initiated. Briefing: 'The user's payment won't go through.']

# Final Reply From: Billing Agent
# Final Message: It looks like your payment failed. I'll transfer you to a billing agent who can help you resolve this.
if __name__ == "__main__":
    main()
