
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,trace,function_tool,RunConfig
from dotenv import load_dotenv
import asyncio
load_dotenv()
# ONLY FOR TRACING
openai_key = os.getenv("OPENAI_API_KEY", "")

os.environ["OPENAI_API_KEY"] = openai_key  # → key system environment variable me set kar deta hai, taki libraries ya doosre modules bhi usko directly use kar saken.(temporarily), Tracing tabhi chalega jab required API key system ke environment variables me set ho, warna tracing service ko pata hi nahi chalega ki tumhara app kahan se aa raha hai.--->os.environ ek bridge hai jahan hum apne Python program me environment variables ko read/write kar sakta hai.

# gemini api key , for model calling
gemini_api_key = os.getenv("GEMINI_API_KEY","")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash"
)
@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    model=llm_model,
    tools=[get_weather]
)

new_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    model=llm_model,
    tools=[get_weather]
)
agent = Agent(
    name="Joke generator",
    instructions="Tell funny jokes.",
    model=llm_model
)

async def main():

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke")
        joke = first_result.final_output
        second_result = await Runner.run(agent, f"Rate this joke: {joke}",run_config=RunConfig(tracing_disabled=True))  # run_congig-->disabled this agent tracing , tracing rating not in "trace" 
        print(f"Joke: {joke}")
        print(f"Rating: {second_result.final_output}")
asyncio.run(main())

    # Now check the trace in 