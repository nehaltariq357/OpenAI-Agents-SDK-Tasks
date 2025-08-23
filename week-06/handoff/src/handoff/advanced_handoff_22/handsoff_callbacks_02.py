import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel


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
class NewsRequest(BaseModel):
    topic:str
    reason:str

@function_tool
def get_weather(city:str):
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


def on_news_transfer(ctx: RunContextWrapper, input_data: NewsRequest) -> None:
    print(f"\nTransferring to for news updates. input_data:", input_data, "\n")


def on_news_transfer(ctx:RunContextWrapper,input_data):
    print(f"\nTransferring to for news updates. input_data:", input_data, "\n")

news_agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me.",
    model=model,
    tools=[get_weather]
)

weather_agent = Agent(
    name="WeatherAgent",
    instructions=(
        "You are weather expert - share weather updates as I travel a lot."
        "For all Tech and News let the NewsAgent handle that part by delegation."
),
    model=model,
    tools=[get_weather],
    handoffs=[handoff(agent=news_agent,on_handoff=on_news_transfer,input_type=NewsRequest)]
)
def handsoff_callbacks():

    result = Runner.run_sync(
        starting_agent=weather_agent,
        input="Check if there's any news about OpenAI after GPT-5 launch?",
    )

    print("\nAGENT NAME: ", result.last_agent.name)
    print("\n[RESPONSE:]", result.final_output)

    
if __name__ == "__main__":
    handsoff_callbacks()
