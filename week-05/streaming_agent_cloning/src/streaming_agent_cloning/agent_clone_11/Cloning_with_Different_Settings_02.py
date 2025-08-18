import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,ModelSettings
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

def main():

    # base agent 
    base_agent = Agent(
    name="BaseAssistant",
    instructions="you are helpful assistant",
    model=model,
    model_settings=ModelSettings(temperature="0.7")   
)
    
    # Clone with different temperature

    creative_agent = base_agent.clone(
        name="creativeAssistant",
        instructions = "You are a creative writing assistant.",
        model_settings = ModelSettings(temperature=0.9)  # Higher creativity
    )

    precise_agent = base_agent.clone(
        name="PreciseAssistant", 
        instructions="You are a precise, factual assistant.",
        model_settings=ModelSettings(temperature=0.1)  # Lower creativity
    )

    # Test creativity levels
    query = "Describe a sunset."

    result_creative = Runner.run_sync(
        starting_agent=creative_agent,
        input=query
    )

    result_precise = Runner.run_sync(
        starting_agent=precise_agent,
        input=query
    )

    print("\nCreative:\n", result_creative.final_output)
    print("\nPrecise:\n", result_precise.final_output)