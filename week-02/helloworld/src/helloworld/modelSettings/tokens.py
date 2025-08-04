
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,ModelSettings
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

    agent_brief = Agent(
        name="Brief Bot",
        model_settings=ModelSettings(max_tokens=100)
    )

    agent_detailed = Agent(
    name="Brief Bot",
    model_settings=ModelSettings(max_tokens=1000)
    )
    question = "Intruduce yourself and answers what is AI"

    print("\nBrief Bot:")
    brief = Runner.run_sync(agent_brief,question,run_config=config)
    print(brief.final_output)

    print("\nDetailed Bot:")
    detail = Runner.run_sync(agent_detailed,question,run_config=config)
    print(detail.final_output)


if __name__ == "__main__":
    asyncio.run(main())