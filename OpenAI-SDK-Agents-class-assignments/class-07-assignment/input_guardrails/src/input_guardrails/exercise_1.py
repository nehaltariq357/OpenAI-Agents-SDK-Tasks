import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    set_tracing_disabled
)

set_tracing_disabled(disabled=True)
# Agent (normal assistant)
from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,Agent,Runner
set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)
student_agent = Agent(
    name="Student Agent",
    instructions="You are a student helper agent."
)

# Input Guardrail function
@input_guardrail
async def class_timing_guardrail(ctx, agent, input: str):
    # agar input me "change my class timings" phrase mila toh trigger karo
    if "change my class timings" in input.lower():
        return GuardrailFunctionOutput(
            output_info="Request to change class timings detected.",
            tripwire_triggered=True
        )
    
    # warna allow karo
    return GuardrailFunctionOutput(
        output_info="Input is safe.",
        tripwire_triggered=False
    )

# Attach guardrail to agent
main_agent = Agent(
    name="Main Agent",
    instructions="You are a helpful assistant.",
    input_guardrails=[class_timing_guardrail]
)

# Main function
async def main():
    try:
        result = await Runner.run(
            main_agent,
            "I want to change my class timings 😭😭",  #  ye guardrail trigger karega
        )
        print(" Agent Output:", result.final_output)

    except InputGuardrailTripwireTriggered:
        print(" Guardrail Triggered: Input not allowed")

if __name__ == "__main__":
    asyncio.run(main())
