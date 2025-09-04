from dotenv import load_dotenv
import os
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    Agent,
    Runner,
    function_tool,
)
import requests

# Disable tracing
set_tracing_disabled(disabled=True)

# Load environment variables
load_dotenv()

# Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please add it in your .env file.")

# External client setup
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)


# Tool for fetching products
@function_tool
def get_products(name: str = None):
    """
    Fetch products from the Hackathon API.
    If `name` is provided, return only products that match (case-insensitive).
    """
    url = "https://hackathon-apis.vercel.app/api/products"
    try:
        response = requests.get(url, timeout=10)
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

    if response.status_code != 200:
        return {"error": f"Failed to fetch products, status code: {response.status_code}"}

    products = response.json()

    if name:
        filtered = [p for p in products if name.lower() in p["name"].lower()]
        return filtered if filtered else {"message": f"No product found for '{name}'"}

    return products


# Agent setup
agent = Agent(
    name="Shopping Assistant",
    instructions=(
        "You are a shopping assistant. "
        "When asked about products, always use the get_products tool. "
        "Format responses in a user-friendly way. "
        "If multiple products are returned, list them with name, price, and category. "
        "If no product is found, politely tell the user."
    ),
    tools=[get_products],
    model=model,
)


# Main runner
def main():
    queries = [
        "show me all products",
        "find me Wood Chair",
        "find me iPhone",
    ]

    for q in queries:
        print(f"\n Query: {q}")
        result = Runner.run_sync(
            starting_agent=agent,
            input=q,
        )
        print(" Response:", result.final_output)


if __name__ == "__main__":
    main()
