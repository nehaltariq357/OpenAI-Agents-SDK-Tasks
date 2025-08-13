import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,RunContextWrapper,function_tool
from dotenv import load_dotenv
from dataclasses import dataclass
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

@dataclass
class UserContext:
    username: str
    email: str | None = None
@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    import time
    time.sleep(30)  # Simulating a delay for the search operation
    return "No results found."

async def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    # who is user?
    # which agent
    
    print(f"\nUser: {special_context.context.username},\n Agent: {agent.name}\n")
    return f"You are a math expert. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."

def main():
    # Call the agent with a specific input
    user_context = UserContext(username="abdullah")
    agent = Agent(
    name="Gemius",
    instructions=special_prompt,
    model=model,
    tools=[search]
)

    result = Runner.run_sync(
        starting_agent=agent,
        input="search for the best math tutor in my area",
        context=user_context

    )

    print(result.final_output)