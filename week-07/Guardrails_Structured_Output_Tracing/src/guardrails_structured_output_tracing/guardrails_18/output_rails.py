import os
from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    set_tracing_disabled,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    output_guardrail
)

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
    model="gemini-2.0-flash",
)
class SensitivityCheck(BaseModel): 
    contains_sensitive_info: bool
    reasoning: str
    confidence_level: int  # 1-10 scale
class MessageOutput(BaseModel): 
    response: str

output_guardrail_agent = Agent(
    name="Privacy Guardian",
    instructions=""" 
    Check if the response contains:
    - Personal information (SSN, addresses, phone numbers)
    - Internal company information
    - Confidential data
    - Inappropriate personal details
    
    Be thorough but not overly sensitive to normal business information.

""",
    model=model,
    output_type=SensitivityCheck
)

@output_guardrail
async def privacy_guardrail(ctx:RunContextWrapper[None],agent:Agent,output:MessageOutput,)->GuardrailFunctionOutput:
    # Check the agent's response for sensitive content
    result = await Runner.run(starting_agent=output_guardrail_agent,input=f"Please analyze this customer service response:{output.response}",context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered= result.final_output.contains_sensitive_info  # aspect boolen value
    )
# Main customer support agent with output guardrail
support_agent = Agent(
    name="Customer Support Agent",
    instructions="Help customers with their questions. Be friendly and informative.",
    model=model,
    output_type=MessageOutput,
    output_guardrails=[privacy_guardrail]   #Add our privacy check
)
async def test_privacy_protection():
    try:
        await asyncio.sleep(6)  # add delay to stay under quota (10 req/min)
        result = await Runner.run(
            starting_agent=support_agent,
            input="What's my account status for john.doe@email.com?",
        )
        print(f"✅ Response approved: {result.final_output.response}")
    except OutputGuardrailTripwireTriggered:
        print("🛑 Response blocked - contained sensitive information!")
        fallback_message = "I apologize, but I need to verify your identity before sharing account details."
        print(f"Fallback: {fallback_message}")



asyncio.run(test_privacy_protection())