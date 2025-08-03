from agents import Agent,OpenAIChatCompletionsModel,AsyncOpenAI,Runner
import os
import asyncio
from agents.run import RunConfig
from dotenv import load_dotenv
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found. Make sure your .env file is correct.")


client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client

)

config = RunConfig(
    model_provider=client,
    model=model,
    tracing_disabled=True,
)
async def main():
    agent = Agent(    
    name="Assistant",
    instructions="you are helpful assistant.",
    model=model,
)
    prompt = "Hi, please introduce yourself. Also, what is AI?"

    output =await Runner.run(
        agent,
        prompt,
        run_config=config
    )

    print(output.final_output)

# 👇 Add this
if __name__ == "__main__":
    asyncio.run(main())