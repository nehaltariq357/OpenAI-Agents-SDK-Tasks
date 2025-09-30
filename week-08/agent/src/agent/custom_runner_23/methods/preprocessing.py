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
    async def run(self,starting_agent,input,**kwargs):

        # Preprocessing logic
        print(f"[PRE] User input received: {input}")

        # Example: routing based on keywords
        if "finance" in str(input).lower():
            print("[ROUTING] Sending to Finance Agent")
            starting_agent.instructions = "you are a financial expert."
        elif "health" in str(input).lower():
            print("[ROUTING] Sending to Health Agent")
            starting_agent.instructions= "You are a medical assistant."

        # Core execution
        result= await super().run(starting_agent, input, **kwargs)
        return result
    
Finance = Agent(
        name="Assistant",
        model=model,
    )
Health_agent = Agent(
        name="Assistant",
        model=model,
    )
    

set_default_agent_runner(MyCustomRunClass()) #() is necessary

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant with memory.",
        model=model,
    )
    # custom runner
    result =await Runner.run(agent,input="hello Finance Agent")
    print(result.final_output)  # [ROUTING]----> Sending to Finance Agent

asyncio.run(main())
