

import os
from dataclasses import dataclass
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,RunContextWrapper,function_tool
import asyncio
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()
# this class use as a context
@dataclass
class UserInfo:
    username :str
    email:str
# tool
@function_tool
def browse(context:RunContextWrapper) -> str:
    """"Search from the browser."""
    print("context = ", context)
    return "No reseul found"

user = UserInfo (username = "Nehal Tariq",email="abc@gmail.com")

def dynamic_instruction(wrapper:RunContextWrapper[UserInfo],agent:Agent):
    print("\nFrom Dynamic Instructions\n")
    # wrapper.context me wahi object aata hai jo tumne context= me bheja
    print("wrapper = ", wrapper.context)
    print("agent = ", agent)
    return f"you are a python expert. And user name is {wrapper.context.username} and email is {wrapper.context.email}"
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
    agent = Agent(
        name = "python_expert",
        instructions=dynamic_instruction,
        model=model,
        tools=[browse]
    )
    
    result = Runner.run_sync(
        starting_agent = agent,
        input = "hi, what is the username and email",
        run_config=config,
        context =user  # <--- yahan se tum apna context data bhejte ho
    )
    
    print(result.final_output) # Your username is Nehal Tariq and your email is abc@gmail.com.

if __name__ == "__main__":
    main()