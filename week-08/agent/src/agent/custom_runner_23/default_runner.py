import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper

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


def main():
    agent = Agent(
        name="Assistant",
        instructions="""You are a helpful assistant with memory.""",
        model=model,
    )
    text = "hello"
    # default runner
    result = Runner.run_sync(
        starting_agent=agent,
        input=text,

    )

    print(result.final_output)
