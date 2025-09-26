import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from agents.tool_context import ToolContext
from dataclasses import dataclass
from mem0 import MemoryClient


@dataclass
class UserContext:
    username: str

_: bool = load_dotenv(find_dotenv())

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
memo_api_key  = os.getenv("memo_api_key")

memo = MemoryClient(api_key=memo_api_key)

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model= OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def add_memory(query: str, user_id: str) -> str:
    return memo.add([{"role": "user", "content": query}], user_id=user_id)

@function_tool
def search_memory(query: str, user_id: str) -> str:
    return memo.search(query, user_id=user_id, limit=3)

def main():
    agent = Agent(
        name="Assistant",
        instructions="""You are a helpful assistant with memory.
        Always check memory first before answering.
        Save new details about the user whenever possible.""",
        model=model,
        tools=[add_memory,search_memory]
    )
    text = "What is my name and what I like to do and user_id is `nehal_123`?"
    result = Runner.run_sync(
        starting_agent=agent,
        input=text,

    )

    print(result.final_output)
