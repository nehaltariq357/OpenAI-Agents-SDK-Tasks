#  Assignment:
#  Create an agent with a calculator tool that answers math queries using your Python 
# function.
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,Runner,function_tool,set_tracing_disabled
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
def calculator(n1:int,n2:int,operation:str)->str:
    """
    Calculator tool that answers math queries.
    Follows DMAS rule: Division, Multiplication, Addition, Subtraction.
    operation: '+', '-', '*', '/'
    """
    print("calculator tool fire------->")

    if operation == "/":
        result = n1 / n2
    elif operation == "*":
        result = n1 * n2
    elif operation == "+":
        result = n1 +n2
    elif operation == "-":
        result = n1-n2
    else:
        return "Invalid operation"
    return f"The answer is {result}"
    
@function_tool

def get_weather(city: str) -> str:
    """
    Weather tool that provides weather conditions.
    """
    print("weather tool fire-------->")
    return {
        "temp":33,
        "condition":"cloudy"
    }



def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Always use tools for math questions. And for weather conditions"
                    "Always follow DMAS rule (division, multiplication, addition, subtraction)."
                    "Explain answers clearly and briefly for beginners.",
        model=model,
        tools=[calculator,get_weather] # providing tools
    )
    # 🧪 5) Run the agent with a prompt (tool calling expected)
    while True:
        
        prompt = input("user:" ).strip().lower()

        if prompt in ["bye","exit","quit"]:
            print("bye")
            break

        result = Runner.run_sync(
            starting_agent=agent,
            input=prompt,
            
        )
        # 📤 Print the final result from the agent
        print("\n🤖 CALLING AGENT\n")
        print("Bot= ",result.final_output)  