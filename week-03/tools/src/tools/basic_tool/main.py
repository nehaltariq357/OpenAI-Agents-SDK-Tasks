import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,Runner,function_tool,ModelSettings
from dotenv import load_dotenv
# 🌿 Load environment variables from .env file
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL_VAR = os.getenv("BASE_URL")
if not GEMINI_KEY:
    raise ValueError("gemini key is not in env")
if not BASE_URL_VAR:
    raise ValueError("BASE_URL is not in env")

gemini_clinet = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url=BASE_URL_VAR
)


model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client=gemini_clinet

)

config = RunConfig(
    model=model,
    model_provider=gemini_clinet,
    tracing_disabled=True
)
# 🛠️ 3) Define tools (functions wrapped for tool calling)
@function_tool
def multiply(a:int,b:int):
    """🧮 Exact multiplication (use this instead of guessing math)."""
    return a*b

@function_tool
def sum(a:int,b:int):
    """➕ Exact addition (use this instead of guessing math)."""
    return a+b


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. "
        "Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). "
        "Explain answers clearly and briefly for beginners.",
        model=model,
        model_settings=ModelSettings(tool_choice="required"),
        tools=[multiply,sum] # providing tools
    )
    # 🧪 5) Run the agent with a prompt (tool calling expected)
    prompt = "what is 19 + 23 * 2?"

    result =await Runner.run_streamed(
        starting_agent=agent,
        input=prompt,
        run_config=config
    )
    # 📤 Print the final result from the agent
    print("\n🤖 CALLING AGENT\n")
    print("Bot= ",result.final_output)  