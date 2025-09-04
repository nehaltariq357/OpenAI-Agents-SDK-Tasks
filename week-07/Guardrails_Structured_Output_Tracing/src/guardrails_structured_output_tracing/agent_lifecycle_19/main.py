import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, AgentHooks, RunContextWrapper
from rich import print
load_dotenv(find_dotenv())

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Agent Lifecycle Callbacks/Hooks

class MyAgentHooks(AgentHooks):

    def __init__(self,lifecycle_name:str):   #  
        self.lifecycle_name = lifecycle_name

    async def on_start(self,context,agent):
        print(f"{agent.name} started...")

    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"\nagent instruction:{system_prompt}")
        print(f"\nuser input:{input_items}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"\nAI answers: {response}")
    
    async def on_tool_start(self, context, agent, tool):
        print(f"\ntool name: {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"tool output: {result}")
    
    async def on_handoff(self, context, agent, source):
        print(f"task handover to: {source}")
    
    async def on_end(self, context, agent, output):
        print(f"\n agent name: {agent.name}")
        print(f"\nfinal answer: {output}")
    
@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny." 
    
news_agent = Agent(
    name="NewsAgent",
    instructions="You handle news related queries",
    model=llm_model,
    hooks=MyAgentHooks("NewsAgentLifecycle")
)    
agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. Talk about weather and let news_agent handle the news things",
    model=llm_model,
    tools=[get_weather],
    handoffs=[news_agent],
    hooks=MyAgentHooks("WeatherAgentLifecycle")   # 👈 yaha hooks attach karte hain
)

def main():
    res = Runner.run_sync(agent, "What's the latest news about Qwen Code - seems like it can give though time to claude code.")
    print(res.last_agent.name)
    print(res.final_output)

    print(res.final_output)