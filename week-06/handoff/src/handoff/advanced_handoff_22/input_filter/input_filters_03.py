import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,handoff,function_tool,RunContextWrapper
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




agent = Agent(
    name="assistant",
    instructions="You are a helpful assistant",
    model=model,
    
)


def input_filters():

    result = Runner.run_sync(
        starting_agent=agent,
        input="hello ",
    )

    
    print(result.final_output)

    
if __name__ == "__main__":
    input_filters()
