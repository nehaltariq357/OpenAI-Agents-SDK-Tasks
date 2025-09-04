import asyncio
import re
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

# ---------------- Father Guardrail ----------------
@input_guardrail
async def father_guardrail(ctx, agent, input: str):
    """
    Father stops child if temperature is below 26°C.
    Uses regex to catch 20C, 20°C, 20 c, etc.
    """
    match = re.search(r"(\d+)\s?°?c", input.lower())
    if match:
        temp = int(match.group(1))
        if temp < 26:
            return GuardrailFunctionOutput(
                output_info=f"🚫 Son, {temp}°C is too cold for running! You might catch a cold. Stay home instead.",
                tripwire_triggered=True
            )
        else:
            return GuardrailFunctionOutput(
                output_info=f"✅ {temp}°C is safe. Go enjoy your run, but stay hydrated!",
                tripwire_triggered=False
            )

    return GuardrailFunctionOutput(
        output_info="⚠️ You didn’t mention the temperature. Please specify.",
        tripwire_triggered=True
    )

# ---------------- Agents ----------------
child_agent = Agent(
    name="Child Agent",
    instructions="You are a child asking your father if you can run.",
    input_guardrails=[father_guardrail],
    model=model
)

# ---------------- Main ----------------
async def main():
    # ❌ Case 1: Below 26°C -> Father stops
    try:
        result = await Runner.run(child_agent, "Father, can I run outside at 20C?")
        print("🤖 Response:", result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("🚨 Guardrail Triggered: not allowed below 20C")

    # ✅ Case 2: Above 26°C -> Allowed
    try:
        result = await Runner.run(child_agent, "Father, can I run outside at 28C?")
        print("🤖 Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🚨 Guardrail Triggered: not allowed below 20C")

if __name__ == "__main__":
    asyncio.run(main())
