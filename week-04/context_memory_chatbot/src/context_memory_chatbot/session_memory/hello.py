
import os
from dotenv import load_dotenv
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,SQLiteSession
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)
external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

def main():
    agent = Agent(
        name="Assistant",
        instructions="you are helpful assistant",
        model=model
    )

    # create session memory

    session = SQLiteSession("my_first_conversation")

    print("=== First Conversation with Memory ===")

    # turn - 01

    result1 = Runner.run_sync(
        starting_agent=agent,
        input="Hi! My name is Alex and I love pizza",
        session=session
    )
    print("Agent:",result1.final_output) #Agent: Hi Alex! It's great to meet another pizza lover!

    # turn - 02

    result2 = Runner.run_sync(
        starting_agent=agent,
        input="What's my name?",
        session=session
    )
    print("Agent:",result2.final_output) # Agent: Your name is **Alex**!

    # turn - 03
    
    result3 = Runner.run_sync(
        starting_agent=agent,
        input="What food do I like?",
        session=session
    )
    print("Agent:",result3.final_output) #Agent: You love **pizza**!