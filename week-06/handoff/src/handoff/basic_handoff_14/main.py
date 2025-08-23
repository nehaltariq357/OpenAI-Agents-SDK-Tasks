import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff
from dotenv import load_dotenv
from rich import print



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
billing_agent = Agent(
    name="Billing Agent",
    instructions="Handle billing questions.",
    model=model
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="Handle refunds.",
    model=model
)

triage_agent = Agent(
    name="Assistant",
    instructions=(
        "Greet the user and decide where to send them:\n"
        "- If the user asks about a double charge, invoice, payment, etc., hand off to Billing Agent.\n"
        "- If the user asks about refund status or returning an item, hand off to Refunds Agent.\n"
        "Once handed off, the specialist should continue the conversation."
    ),
    model=model,
    handoffs=[billing_agent,handoff(agent=refund_agent)]  # either direct agent or `handoff(...)`
    
)

def basic_handoff():
    result = Runner.run_sync(
        starting_agent=triage_agent,
        input="My card was charged twice",
    )
    print(" look for HandoffCallItem then HandoffOutputItem (proof a handoff occurred): ",result.new_items)
    print("who actually answered: ",result.last_agent)  #who actually answered Agent(name='Billing Agent', handoff_description=None,
    print(result.final_output)
    
    
if __name__ == "__main__":
    basic_handoff()
