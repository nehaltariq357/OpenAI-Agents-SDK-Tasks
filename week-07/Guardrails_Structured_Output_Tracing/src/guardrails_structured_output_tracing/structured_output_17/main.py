import os
from agents import Agent,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

class WeatherAnswer(BaseModel):
    location:str
    temperature_c:float
    summary:str




agent = Agent(
    name="assistant",
    instructions="you are ahelpful assistant",
    model=model,
    output_type=WeatherAnswer
)

def main():
    result = Runner.run_sync(
        starting_agent=agent,
        input="What's the weather in Karachi?",
    )


    print(result.final_output.location)
    print(result.final_output.temperature_c)
    print(result.final_output.summary)


if __name__ == "__main__":
    main()

# Remember: Structured output transforms your agent from giving messy text to providing perfect, usable data every time! 📊✨




