import time
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio
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

async def streaming_msg():

    agent = Agent(
    name="Joker",
    instructions="You are a funny assistant.",
    model=model,
    
)

    result = Runner.run_streamed(
        starting_agent=agent,
        input="Please tell me 5 jokes.",
    )

    # async for event in result.stream_events():
    #     if event.item.type == "message_output_item":
    #         print(ItemHelpers.text_message_output(event.item))

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)
            time.sleep(0.5)

asyncio.run(streaming_msg())