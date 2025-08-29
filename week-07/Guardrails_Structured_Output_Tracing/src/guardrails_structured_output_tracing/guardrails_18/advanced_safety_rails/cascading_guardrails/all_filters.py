import os
import asyncio
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,input_guardrail,GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem,InputGuardrailTripwireTriggered
from dotenv import load_dotenv,find_dotenv
from pydantic import BaseModel
load_dotenv(find_dotenv())

set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv(key="GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


class ProfanityCheck(BaseModel):
    is_toxic: bool
    reasoning: str
    confidence: float  # 0..1

profanity_guard_agent = Agent(
    name="Profanity Detector",
    instructions=(
        "Detect if the user input contains profanity, abusive, or offensive language. "
        "Return True if yes. Give a confidence between 0 and 1."
    ),
    model=model,
    output_type=ProfanityCheck
)

@input_guardrail
async def profanity_filter(
    ctx:RunContextWrapper[None],
    agent = Agent,
    input = str | list[TResponseInputItem]
)->GuardrailFunctionOutput:
    result = await Runner.run(
        profanity_guard_agent,
        input,
        context=ctx.context
    )
    check = result.final_output
    # threshold decide karna important hai
    TRIPWIRE = check.is_toxic and check.confidence >= 0.6
    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=TRIPWIRE
        # user_message="⚠️ Please avoid offensive language."
    )
    


support_agent = Agent(
    name="Customer Support Agent",
    instructions="You help users with customer support for our software product. Be concise and friendly.",
    model=model,
    input_guardrails=[profanity_filter], # profanity_filter,topic_validator,rate_limiter
    output_guardrails=[] # privacy_checker,quality_validator,brand_compliance
)


async def all_filters():
    try:
        # ye input guardrail ko trigger karega
        result =await Runner.run(
            starting_agent=support_agent,
            input= "you are stupid idiot!",
        )
        print("Response:", result.final_output)
    except InputGuardrailTripwireTriggered:
        print("🛑 Blocked by profanity_filter")  # 🛑 Blocked by profanity_filter ---> printss

if __name__ =="__main__":
    asyncio.run(all_filters())


