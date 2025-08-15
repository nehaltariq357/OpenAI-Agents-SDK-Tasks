import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner
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

    agent = Agent(
    name="Assistant",
    instructions="you are helpful assistant",
    model=model,
    
)

    result = Runner.run_sync(
        starting_agent=agent,
        input="what is AI",

    )

    print(result.final_output)