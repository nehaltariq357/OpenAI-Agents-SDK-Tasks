
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,ModelSettings,function_tool
import asyncio
from agents.run import RunConfig
from dotenv import load_dotenv

load_dotenv()

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
# 🛠️ Simple tool for learning
@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle."""
    area = length * width
    return f"Area = {length} × {width} = {area} square units"
def main():
    
    
    # Example 2: Tool Choice
    print("\n🔧 Tool Choice Settings")
    print("-" * 30)


agent_auto = Agent(
        name="Auto",
        tools=[calculate_area] , #calculatate_area
        model_settings=ModelSettings(tool_choice="auto")
        )

agent_required = Agent(
        name="Forced Tool Agent",
        tools=[calculate_area] , #calculatate_area
        model_settings=ModelSettings(tool_choice="required")
        )

agent_no_tools = Agent(
        name="Chat Only",
        tools=[calculate_area] , #calculatate_area
        model_settings=ModelSettings(tool_choice="none")
        )

question = "What's the area of a 5x3 rectangle?"

print("Auto Tool Choice:")
result_auto = Runner.run_sync(agent_auto,question,run_config=config)
print(result_auto.final_output)

print("\nRequired Tool Choice:")
result_required = Runner.run_sync(agent_required,question,run_config=config)
print(result_required.final_output)

print("\nNone Tool Choice:")
result_none = Runner.run_sync(agent_no_tools,question,run_config=config)
print(result_none.final_output)
if __name__ == "__main__":
    asyncio.run(main())