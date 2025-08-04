

import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,RunContextWrapper
import asyncio
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY is not set")


external_clinet = AsyncOpenAI(
    api_key = gemini_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
   
)


model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client = external_clinet,
)

config = RunConfig(
    model = model,
    model_provider = external_clinet,
    tracing_disabled = True,
)

def main():
    '''Learn Dynamic Instructions with simple examples'''
    print("🎭 Dynamic Instructions: Make your agent adapt")
    print("-"*50)

    # 🎯 Example 1: Basic Dynamic Instructions

    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)

    # we use here only agent:Agent , not context, we will use it in example 2 after learn it.
    def basic_dynamic(context:RunContextWrapper,agent:Agent):
        """Basic dynamic instructions function."""
        return f"You are {agent.name}. Be helpful and friendly." # You are Dynamic Agent. Be helpful and friendly.
    
    agent_basic = Agent(
        name= "Dynamic Agent",
        instructions=basic_dynamic,
        model=model
    )
    prompt = "Hello"
    result = Runner.run_sync(agent_basic,prompt,run_config=config)
    print("Basic Dynamic Agent:")
    print(result.final_output)
        

if __name__ == "__main__":
    asyncio.run(main())