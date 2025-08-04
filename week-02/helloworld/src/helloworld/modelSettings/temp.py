
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,ModelSettings
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

def main():
    '''Learn model settings with simple examples'''
    #  Example 1: Temperature (Creativity Control)
    print("\n❄️🔥 Temperature Settings")
    print("-" * 30)

    agent_cold = Agent(
        name="Cold Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(temperature=0.1),
        model=model
    )

    agent_hot = Agent(
        name="Hot Agent",
        instructions="You are a helpful Assistant",
        model_settings=ModelSettings(temperature=1.9)
    )

    question = "Tell me about AI in 2 sentences"
    
    print("Cold Agent (Temperature = 0.1):")
    result_cold = Runner.run_sync(agent_cold, question,run_config=config)
    print(result_cold.final_output)
    
    print("\nHot Agent (Temperature = 1.9):")
    result_hot = Runner.run_sync(agent_hot, question,run_config=config)
    print(result_hot.final_output)
    
    print("\n💡 Notice: Cold = focused, Hot = creative")
    print("📝 Note: Gemini temperature range extends to 2.0")

if __name__ == "__main__":
    asyncio.run(main())