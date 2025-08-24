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
    print("\n\n....news_items mila...\n\n")
    print("[ORIGINAL pre_handoff_items]:", data.new_items)
    
    
    print("\n\n[ITEM 1]", data.input_history)
    print("\n\n[ITEM 2]", data.pre_handoff_items)
    print("\n\n[ITEM 3]", data.new_items)

    # sirf pehla item bhejna hain
    trimmed_new = data.new_items[:1]
    print("\n[FILTERED pre_handoff_items]:", trimmed_new)
    return HandoffInputData(
        input_history=data.input_history,  # pora context waisa ka waisa
        pre_handoff_items=data.pre_handoff_items, # pora context waisa ka waisa
        new_items=trimmed_new, # sirf ek naya item bhejna ---> news agents handoff ke time
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

def new_items():

    res = Runner.run_sync(weather_agent, "Check if there's any news about OpenAI after GPT-5 launch?")
    print("\nAGENT NAME", res.last_agent.name)
    print("\n[RESPONSE:]", res.final_output)


if __name__ == "__main__":
    new_items()


