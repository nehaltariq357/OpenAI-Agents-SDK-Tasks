
import requests
import os
from agents import Agent, Runner, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel

set_tracing_disabled(disabled=True)
load_dotenv()

# External Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Please set GEMINI_API_KEY in your .env file")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

# Tool to fetch crypto price
@function_tool
def get_crypto_price(coin: str, currency: str = "usd") -> str:
    """
    Fetches the current price of a cryptocurrency in the specified currency.
    Example: get_crypto_price("bitcoin", "usd")
    """
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin.lower(), "vs_currencies": currency.lower()}
    response = requests.get(url, params=params)
    data = response.json()
    if coin.lower() in data:
        return f"1 {coin.capitalize()} = {data[coin.lower()][currency.lower()]} {currency.upper()}"
    return f"Could not fetch price for {coin} in {currency}"

# Define Crypto Agent
agent = Agent(
    name="Crypto Agent",
    instructions=(
        """
        You are a helpful crypto assistant. 
        - If the user asks about a crypto price, call the get_crypto_price tool.
        - Always provide clear, simple answers.
        - Default currency is USD unless user specifies otherwise.
        """
    ),
    model=model,
    tools=[get_crypto_price],
)

def main():
    queries = [
        "What is the price of Bitcoin?",
        "Show me Ethereum price in USD",
        "Tell me the price of Dogecoin in PKR",
    ]

    for q in queries:
        print(f"\n🔹 User: {q}")
        result = Runner.run_sync(agent, q)
        print(f"Agent: {result.final_output}")

if __name__ == "__main__":
    main()
