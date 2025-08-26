
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
from typing import List


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
'''*************************************************************************************************'''

class StructuredResearch(BaseModel):
    notes:List[str]
    sources:List[str]
    agent_name:str

class TaskSpec(BaseModel):
    summary:str
    action_type:str    # e.g., "email", "plan", "todo"
    details: str
    agent_name:str

@function_tool
def fake_search(query: str) -> str:
    """Perform a fake search and return dummy results"""
    return f"Dummy research notes for: {query} | Source: fake.com/{query}"

def log_handoff(context:RunContextWrapper, input):
    print(f"[HANDOFF] {context} → {context}")
    print(f"Payload: {input}\n")

# --- Action Taker Agent ---
action_taker = Agent(
    name="Action Taker Agent",
    instructions=(
        "You will receive a TaskSpec (summary, action_type, details, agent_name). "
        "If action_type is 'email', draft a polite email. "
        "If 'plan', create a step-by-step plan. "
        "If 'todo', output a numbered todo list."
    ),
    model=model,
)

to_action_taker = handoff(
    agent=action_taker,
    input_type=TaskSpec,
    on_handoff=log_handoff,
    tool_name_override=""
)
summarizer_agent = Agent(
    name="Summarizer Agent",
    instructions=(
        "You will receive StructuredResearch (notes + sources + agent_name). "
        "Step 1: Write a concise summary. "
        "Step 2: Decide an action_type: 'email', 'plan', or 'todo'. "
        "Step 3: Wrap the result into TaskSpec and handoff to Action-Taker."
    ),
    model=model,
    handoffs=[to_action_taker]
)

to_summarizer = handoff(
    agent=summarizer_agent,
    input_type=StructuredResearch,  # force structured input
    on_handoff=log_handoff,
    
)



Research_agent = Agent(
    name="Research Agent",
    instructions="You are a research agent. Always use fake_search tool for answering search queries.",
    model=model,
    tools=[fake_search],
    handoffs=[to_summarizer]
)



def main():
    result = Runner.run_sync(
        starting_agent=Research_agent,
        input="Research about benefits of AI in education"
    )

    print(f"\nFinal Output:\n{result.final_output}")
    print(f"\nFinal Reply From: {result.last_agent.name}")



if __name__ == "__main__":
    main()