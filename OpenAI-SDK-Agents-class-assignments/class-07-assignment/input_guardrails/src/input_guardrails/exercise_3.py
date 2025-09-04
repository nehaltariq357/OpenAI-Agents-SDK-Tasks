import asyncio
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
)
from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# External Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

# ---------------- Gate Keeper Guardrail ----------------
@input_guardrail
async def gatekeeper_guardrail(ctx, agent, input: str):
    """
    Gatekeeper stops students of other schools.
    Only 'Shoeby Grammer Secondary School' students are allowed.
    """
    if "shoeby grammer secondary school" not in input.lower():
        return GuardrailFunctionOutput(
            output_info="🚫 You are not from Shoeby Grammer Secondary School. Entry denied!",
            tripwire_triggered=True
        )

    return GuardrailFunctionOutput(
        output_info="✅ Welcome! You are from Shoeby Grammer Secondary School, you may enter.",
        tripwire_triggered=False
    )

# ---------------- Agents ----------------
gatekeeper_agent = Agent(
    name="Gatekeeper Agent",
    instructions="You are a strict gatekeeper. Only students of Shoeby Grammer Secondary School are allowed.",
    input_guardrails=[gatekeeper_guardrail],
    model=model
)

# ---------------- Main ----------------
async def main():
    # ❌ Case 1: Other school student
    try:
        result = await Runner.run(gatekeeper_agent, "I am from Blue Sky School.")
        print("🤖 Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🚨 Guardrail Triggered: not allowed")

    # ✅ Case 2: Shoeby student
    try:
        result = await Runner.run(gatekeeper_agent, "Hello, I am a student of Shoeby Grammer Secondary School.")
        print("🤖 Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🚨 Guardrail Triggered: not allowed")

if __name__ == "__main__":
    asyncio.run(main())
