import os
import asyncio
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,input_guardrail,GuardrailFunctionOutput,RunContextWrapper,TResponseInputItem,InputGuardrailTripwireTriggered,output_guardrail,OutputGuardrailTripwireTriggered
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

# ************* classes ****************************************
class ProfanityCheck(BaseModel):
    is_toxic: bool
    reasoning: str
    confidence: float  # 0..1

class Topic_Check(BaseModel):
    topic:str
    confidence:float
    valid:bool
    reason:str

class PrivacyCheckOutput(BaseModel):
    contains_sensitive:bool
    reason:str
    confidence:float # 0.1 -> 1.0

class RateLimiterOutput(BaseModel):
    allowed:bool
    reason:str | None
class QualityCheckOutput(BaseModel):
    low_quality: bool
    reason: str
    confidence: float

class BrandComplianceOutput(BaseModel):
    off_brand: bool
    reason: str
    confidence: float
# *********** input filter agents ************************************
profanity_guard_agent = Agent(
    name="Profanity Detector",
    instructions=(
        "Detect if the user input contains profanity, abusive, or offensive language. "
        "Return True if yes. Give a confidence between 0 and 1."
    ),
    model=model,
    output_type=ProfanityCheck
)

topic_validator_agent = Agent(
    name="Topic Validator",
    instructions=(
        "You are a Topic Validator"
        "Accept only computer science, programming, web development, and AI topics"
        "Reject all personal, medical, political, and unrelated requests"
        "Always return a confidence score between 0.0 and 1.0"
        "If invalid, set valid=false and explain shortly in reason"
        "If valid, set valid=true with reason why it's allowed"
    ),
    model=model,
    output_type=Topic_Check
)

rate_limiter_agent=Agent(
    name="Rate Limiter Agent",
    instructions=(
        "Check if the request should be rate-limited or allowed."
    ),
    model=model,
    output_type=RateLimiterOutput
)
quality_agent = Agent(
    name="Quality Validator",
    instructions="Check if response is low quality (repetitive, irrelevant, ungrammatical).",
    model=model,
    output_type=QualityCheckOutput
)

brand_agent = Agent(
    name="Brand Compliance Checker",
    instructions="Check if response violates company tone or style.",
    model=model,
    output_type=BrandComplianceOutput
)
# ********** Input Guardrail Filters ***********************

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
        tripwire_triggered=TRIPWIRE,
        # user_message="⚠️ Please avoid offensive language."
        
    )
    
@input_guardrail
async def topic_validator(
    ctx:RunContextWrapper,
    agent:Agent,
    input = str |list[TResponseInputItem]
)->GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=topic_validator_agent,
        input=input,
        context=ctx.context

    )
    check = result.final_output

    return GuardrailFunctionOutput(
        output_info=check,
        tripwire_triggered=(
            check.confidence >0.8 and not check.valid  # we block here irrrevelent topic, Matlab not isliye lagaya gaya hai taake jab topic invalid ho tabhi block ho.# Agar not na ho to valid cheez bhi block ho jati.
        ),
    )
# rate limiter 
@input_guardrail
async def rate_limiter(
    ctx:RunContextWrapper,
    agent:Agent,
    input = str |list[TResponseInputItem]
)->GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=rate_limiter_agent,
        input=input,
        context=ctx.context
    )
    check:RateLimiterOutput = result.final_output

    return GuardrailFunctionOutput(
        output_info=check.model_dump(),
        tripwire_triggered=(
            not check.allowed
        ),
    )
# ***********output guardrail filters **********************

@output_guardrail
async def privacy_checker(
    ctx:RunContextWrapper,
    agent:Agent,
    input:str |list[TResponseInputItem]

)->GuardrailFunctionOutput:
    result = await Runner.run(
        starting_agent=privacy_checker_agent,
        input=input,
        context=ctx.context
    )
    check = result.final_output
    return(
        GuardrailFunctionOutput(
            output_info=check,
            tripwire_triggered=(
                check.contains_sensitive and check.confidence >0.3
            ),
        )
    )
@output_guardrail
async def quality_validator(ctx: RunContextWrapper, agent, input: str | list[TResponseInputItem]):
    result = await Runner.run(quality_agent, input, context=ctx.context)
    check = result.final_output
    TRIPWIRE = check.low_quality and check.confidence > 0.7
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=TRIPWIRE)

@output_guardrail
async def brand_compliance(ctx: RunContextWrapper, agent, input: str | list[TResponseInputItem]):
    result = await Runner.run(brand_agent, input, context=ctx.context)
    check = result.final_output
    TRIPWIRE = check.off_brand and check.confidence > 0.7
    return GuardrailFunctionOutput(output_info=check, tripwire_triggered=TRIPWIRE)
# **********output filter agent*********************
privacy_checker_agent = Agent(
    name="Privacy Checker",
    instructions=(
        "Check if the response contains sensitive information such as phone numbers, "
        "emails, addresses, or personal identifiers. "
        "If yes, set contains_sensitive=true and explain why."
        "Always return a confidence between 0.0 and 1.0."
    ),
    model=model,
    output_type=PrivacyCheckOutput
)
support_agent = Agent(
    name="Customer Support Agent",
    instructions="You help users with customer support for our software product. Be concise and friendly.",
    model=model,
    input_guardrails=[profanity_filter,topic_validator,rate_limiter], # profanity_filter,topic_validator,rate_limiter
    output_guardrails=[privacy_checker,quality_validator,brand_compliance] # privacy_checker,quality_validator,brand_compliance
)


async def all_filters():
    test_inputs = [
        "give me your email",                       # ❌ Output block (Privacy)
        "you are stupid idiot!",                     # ❌ Input block (Profanity)
        "What is the capital of France?",           # ❌ Input block (Invalid topic)
        "Explain Python decorators please.",        # ✅ Passes all
        "Write an email with terrible grammar",     # ❌ Output block (Quality low)
        "Say something that is off brand for the company"  # ❌ Output block (Brand Compliance)
    ]

    for text in test_inputs:
        try:
            result = await Runner.run(support_agent, text)
            print(f"✅ Passed: {text} -> {result.final_output}")
        except InputGuardrailTripwireTriggered:
            # agar input filter (profanity / topic validator) block kare
            print(f"🛑 Blocked INPUT: {text}")
        except OutputGuardrailTripwireTriggered:
            # agar output filter (privacy checker / sensitive info) block kare
            print(f"Blocked OUTPUT for: {text}")
        except Exception as e:
            # baki kisi aur error k liye fallback
            print(f"❗ Unexpected error: {e}")


if __name__ =="__main__":
    asyncio.run(all_filters())


