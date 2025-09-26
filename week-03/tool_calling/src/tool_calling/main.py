import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,Runner,function_tool,set_tracing_disabled
from dotenv import load_dotenv
# 🌿 Load environment variables from .env file
load_dotenv()
set_tracing_disabled(disabled=True)
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL_VAR =  "https://generativelanguage.googleapis.com/v1beta/openai/"
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
# 🛠️ 3) Define tools (functions wrapped for tool calling)
@function_tool
def multiplys(a:int,b:int)->str:
    """🧮 Exact multiplication (use this instead of guessing math)."""
    print("product tool fire----->")
    return a*b

@function_tool
def additions(a:int,b:int)->str:
    """➕ Exact addition (use this instead of guessing math)."""
    print("add tool fire----->")
    return a+b

def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. "
        "Always use tools for math questions. Always follow DMAS rule (division, multiplication, addition, subtraction). "
        "Explain answers clearly and briefly for beginners.",
        model=model,
        tools=[multiplys,additions], # providing tools
        
    )
    # 🧪 5) Run the agent with a prompt (tool calling expected)
    prompt = "2*2=?"

    result = Runner.run_sync(
        starting_agent=agent,
        input=prompt,
        # run_config=config
    )
    # 📤 Print the final result from the agent
    print("\n🤖 CALLING AGENT\n")
    print("Bot= ",result.final_output)  