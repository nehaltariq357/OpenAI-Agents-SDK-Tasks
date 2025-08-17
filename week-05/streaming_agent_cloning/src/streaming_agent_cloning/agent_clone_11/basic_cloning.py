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

def basic_cloning():

    # base agent 
    base_agent = Agent(
    name="BaseAssistant",
    instructions="you are helpful assistant",
    model=model,
    model_settings=ModelSettings(temperature="0.7")
    
)
    
    # simple clone

    friendly_agent = base_agent.clone(
        name = "FriendlyAssistant",
        instructions = "You are a very friendly and warm assistant."
    )

    # Test both agents
    query = "Hello, how are you?"

    result_base = Runner.run_sync(
        starting_agent=base_agent,
        input=query
    )
    result_friendly = Runner.run_sync(
        starting_agent=friendly_agent,
        input=query
    )

    print("Base Agent:", result_base.final_output)
    print("Friendly Agent:", result_friendly.final_output)