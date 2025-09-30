
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,RunContextWrapper,function_tool
from rich import print
from pydantic import BaseModel
load_dotenv(find_dotenv())


gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model= OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
class MyContext(BaseModel):
    subscription_tier: str
    user_id: int | None = None
    region: str | None = None

def premium_feature_enabled(context: RunContextWrapper, agent: Agent) -> bool:
    ctx: MyContext = context.context
    return ctx.subscription_tier in ["premium", "enterprise"]

@function_tool(is_enabled=premium_feature_enabled)
def get_weather(city:str):
    """weather tool"""
    return f"Weather data for a premium users in {city}"
def main():
    agent = Agent(
        name="Assistant",
    instructions=(
        "You are a helpful assistant. "
        "When asked about weather, you MUST call the `get_weather` tool. "
        "Do not apologize or give alternative answers."
    ),
        model=model,
        tools=[get_weather]
    )
    # Example: Free User (tool disabled)
    result1 = Runner.run_sync(agent,input="What is the weather in Karachi?",context=MyContext(subscription_tier="free",region="PK",user_id=1))
    print("[red]Free User Result:", result1.final_output)  

    # Example: Premium User (tool enabled)
    result2 = Runner.run_sync(agent,input="What is the weather in Karachi?",context=MyContext(subscription_tier="premium",region="US",user_id=2))
    print("[green]Premium User Result:", result2.final_output)
