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
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

set_tracing_disabled(disabled=True)
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
def search_user_memory(context:ToolContext[UserContext],query:str):
    """Use this tool to search user memories."""
    response = memo.search(query=query,user_id = context.context.username,top_k=3)
    return response

@function_tool
def save_user_memory(context:ToolContext[UserContext],query:str):
    """Use this tool to save user memories."""
    response = memo.add(messages=[
        {"role":"user",
        "content":query
        }
    ],
    user_id = context.context.username
    )
    return response

def dynamic_instrctions_generator(context:RunContextWrapper[UserContext],agent:Agent[UserContext])->str:
    response = memo.search(query="General Behavior",user_id = context.context.username,top_k = 3)
    print(response)
    return f"""Helpful Agent that can answer questions. 
            Use search_user_memory to find information and save_user_memory to remember information.
            User Past Memories: {response}
            """
def main():
    agent = Agent(
        name="assistant",
        instructions=dynamic_instrctions_generator,
        model=model,
        tools=[save_user_memory,search_user_memory]
    )
    while True:
        text = input("\n[user:] ")

        if text.lower() in ["exit","bye"]:
            break

        result = Runner.run_sync(
            starting_agent=agent,
            input=text,
            context=UserContext(username="Nehal")
        )
        print( "\n [AGENT:]" , result.final_output) # requirement_completed, question
