import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,ModelSettings,function_tool
from dotenv import load_dotenv
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

@function_tool
def calculate_area(length:float,width:float)->str:
    '''Area calculator tool'''
    print("calculate area tool fired----------->")
    return f"Area = {length*width} square units"

@function_tool
def get_weather(city: str) -> str:
    '''search weather tool'''
    print("weather tool fired----------->")
    return f"Weather in {city}: Sunny, 72°F"
def main():

# Base agent with one tool 
    base_agent = Agent(
    name="BaseAssistant",
    instructions="you are helpful assistant",
    tools=[calculate_area],
    model=model,
)
# Clone with additional tool
    weather_agent = base_agent.clone(
        name = "WeatherAssistant",
        instructions = "You are a weather and math assistant.",
        model= model,
        tools = [calculate_area,get_weather] #new tools list
    )

    # Clone with different tools

    math_agent = base_agent.clone(
        name="MathAssistant",
        instructions = "You are a math specialist.",
        tools = [calculate_area],
        model=model
    )
    
    result_weather = Runner.run_sync(
        starting_agent=weather_agent,
        input = "what the weather in karachi, and whats the area of square, length is 5 and width is 4"
    )
    result_math = Runner.run_sync(
        starting_agent=math_agent,
        input = "whats the area of rectangle, length is 55 and width is 44"
    )

    print("\nWeather Agent:\n",result_weather.final_output)
    print("\nMath Agent:\n",result_math.final_output)