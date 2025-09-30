import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import AgentRunner,set_default_agent_runner
import asyncio
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

class MyCustomRunClass(AgentRunner):
        async def run(
        self,
        starting_agent: Agent,
        input: str | list,
        **kwargs):
            res = await super().run(starting_agent, input,**kwargs)
            return res
    

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant with memory.",
        model=model,
    )
    set_default_agent_runner(MyCustomRunClass())
    # custom runner
    result =await Runner.run(agent,input="hello")
    print(result.final_output)  # Hello! How can I help you today?

asyncio.run(main())
