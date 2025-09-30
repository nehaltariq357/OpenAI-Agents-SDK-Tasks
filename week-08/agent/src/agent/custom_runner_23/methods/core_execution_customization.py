# 2. Core Execution Customization (Retries + Fallback)

import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio
from agents.run import AgentRunner,set_default_agent_runner
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

# 1. Preprocessing Example
class MyCustomRunClass(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        try:
            result= await super().run(starting_agent, input, **kwargs)
        except Exception as e:
            print(f"[ERROR] Agent failed: {e}")

        # Fallback agent
        fallback_agent = Agent(
                name="Fallback",
                instructions="You are a backup assistant. Keep answers short.",
                model=starting_agent.model,
            )
        result = await super().run(fallback_agent,input,**kwargs)
        return result
    

set_default_agent_runner(MyCustomRunClass()) #() is necessary

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant with memory.",
        model=model,
    )
    # custom runner
    result =await Runner.run(agent,input="hello")
    print(result.final_output)  # 

asyncio.run(main())
