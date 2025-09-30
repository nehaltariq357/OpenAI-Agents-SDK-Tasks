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
async def save_to_db(data: dict):
    # Dummy example
    print("[DB] Saving to database:", data)

# 1. Preprocessing Example
class MyCustomRunClass(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        result = await super().run(starting_agent, input, **kwargs)
    
        #postprocessing
        print("[POST] Final Output:", result.final_output)

        #example save to database

        await save_to_db({
            "agent":starting_agent.name,
            "user_input":input,
            "output":result.final_output
        })
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
    print(result.final_output)  

asyncio.run(main())
