import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper,HandoffInputData
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
def summarized_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("\n\n....pre_handoff_items mila...\n\n")
    print("[ORIGINAL pre_handoff_items]:", data.pre_handoff_items)
    
    
    print("\n\n[ITEM 1]", data.input_history)
    print("\n\n[ITEM 2]", data.pre_handoff_items)
    print("\n\n[ITEM 3]", data.new_items)

    # purane items me se sirf tool related rakhne
    filtered= tuple(item for item in data.pre_handoff_items if "tool" in str(item).lower())
    print("\n[FILTERED pre_handoff_items]:", filtered)
    return HandoffInputData(
        input_history=data.input_history,  #same
        pre_handoff_items=filtered,  # sirf filterd items rakhe
        new_items=data.new_items, # pora context waisa ka waisa
    )

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me.",
    model=model,
    tools=[get_weather],
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are weather expert - share weather updates as I travel a lot. For all Tech and News let the NewsAgent handle that part by delegation.",
    model=model,
    tools=[get_weather],
    handoffs=[handoff(agent=news_agent, input_filter=summarized_news_transfer)]
)

def pre_handoff_items():

    res = Runner.run_sync(weather_agent, "Check if there's any news about OpenAI after GPT-5 launch?")
    print("\nAGENT NAME", res.last_agent.name)
    print("\n[RESPONSE:]", res.final_output)


if __name__ == "__main__":
    pre_handoff_items()


