import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,function_tool,ItemHelpers
from dotenv import load_dotenv
import asyncio
import random
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
def how_many_jokes()->int:
    return random.randint(1,10)
async def main():

    agent = Agent(
    name="Joker",
    instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
    tools=[how_many_jokes],
    model=model,
    
)

    result = Runner.run_streamed(
        starting_agent=agent,
        input="Hello",

    )

    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type =="message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}",flush=True)
        else:
            pass # ignore other event types

asyncio.run(main())
print("=== Run complete ===")