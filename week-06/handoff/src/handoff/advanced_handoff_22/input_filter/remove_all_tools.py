import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
from agents.extensions import handoff_filters

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


class MathInput(BaseModel):
    a :int
    b:int

@function_tool

def add_numbers(data:MathInput):
    return str(data.a + data.b)
@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."
math_agent = Agent(
    name="Math Agent",
    instructions="You are a mathematician",
    model=model,
    tools=[add_numbers]
    
)

weather_agent = Agent(
    name="Weather Agent",
    instructions=(
        "You are weather expert - share weather updates as I travel a lot."
        "For maths related queries let the Math Agent handle that part by delegation."
    ),
    tools=[get_weather],
    model=model,
    handoffs=[handoff(
        agent=math_agent,
        input_filter=handoff_filters.remove_all_tools  # it remove tools, if i comment this, tool run perfectly
    )]
)

# query = "what the temperature in karachi"   # --->>  final answer:  The weather for Karachi is sunny. 

query ="2+2"  # ----> final answer:  It seems that the `add_numbers` function in the available tool concatenates the numbers as strings instead of performing a mathematical addition. So, 
# 2+2 is resulting in "22" rather than 4.


def remove_all_tools():

    result = Runner.run_sync(
        starting_agent=weather_agent,
        input=query,
    )

    
    print("who reponse: ",result.last_agent)
    print("final answer: ",result.final_output)

    
if __name__ == "__main__":
    remove_all_tools()
