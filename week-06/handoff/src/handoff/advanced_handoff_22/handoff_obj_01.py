import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper
from dotenv import load_dotenv
from rich import print



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
def log_handoff_event(context:RunContextWrapper):
    print(f"👉 Handoff triggered from WeatherAgent to NewsAgent ")



@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

news_agent = Agent(
    name="News Agent",
    instructions="You get latest news about tech community and share it with me.",
    model=model,
    tools=[get_weather]
)
weather_agent = Agent(
    name="Weather Agent",
    instructions=(
        "You are weather expert - share weather updates as I travel a lot."
        "For all Tech and News let the NewsAgent handle that part by delegation."
),
    tools=[get_weather],
    model=model,
    handoffs=[handoff(
        agent=news_agent,
        on_handoff=log_handoff_event,
    )]
)
def handoff_obj():
    result = Runner.run_sync(
        starting_agent=weather_agent,
        input="Check if there's any news about OpenAI after GPT-5 launch?"
    )
    # print("who answerd: ",result.last_agent) #  → "NewsAgent"
    print(result.final_output) # → NewsAgent ka jawab

    
if __name__ == "__main__":
    handoff_obj()
