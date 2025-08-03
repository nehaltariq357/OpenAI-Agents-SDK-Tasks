
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
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

async def simple_agent():

    agent = Agent(
    name = "Simple Agent",
    instructions = "You are a simple agent that can answer questions and help with tasks.",
    model = model,
    )
    prompt = "Introduce yourself, and answers 'what is AI' "
    output = await Runner.run(agent,prompt,run_config=config)
    print(output.final_output)


if __name__ == "__main__":
    asyncio.run(simple_agent())