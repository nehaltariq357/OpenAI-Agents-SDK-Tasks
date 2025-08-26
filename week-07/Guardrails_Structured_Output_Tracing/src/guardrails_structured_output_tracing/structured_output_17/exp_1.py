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

# Define your data structure
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str




agent = Agent(
    name="assistant",
    instructions="you are ahelpful assistant",
    model=model,
    output_type=PersonInfo   # This is the magic!
)

def main():
    # Test it
    result = Runner.run_sync(
        starting_agent=agent,
        input="Hi, I'm Alice, I'm 25 years old and I work as a teacher.",
    )


    # Now you get perfect structured data!
    print("Type:", type(result.final_output))        # <class 'PersonInfo'>
    print("Name:", result.final_output.name)         # "Alice"
    print("Age:", result.final_output.age)           # 25
    print("Job:", result.final_output.occupation)    # "teacher"     


if __name__ == "__main__":
    main()






