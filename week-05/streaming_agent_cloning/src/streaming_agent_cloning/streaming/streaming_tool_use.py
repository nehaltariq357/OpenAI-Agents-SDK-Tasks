import os
import asyncio
from dataclasses import dataclass
from dotenv import load_dotenv

from agents import (
    Agent,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    Runner,
    function_tool,
    RunContextWrapper,
)

# Load environment variables
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# Disable tracing
set_tracing_disabled(disabled=True)

# Create external OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)


# -------------------------
# Context for each user
# -------------------------
@dataclass
class UserContext:
    username: str
    email: str | None = None


# -------------------------
# Function Tool
# -------------------------
@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> dict[str, str]:
    """
    Provide the user's location based on a query.
    """
    # You could parse query or connect to a real API later
    return {
        "country": "Pakistan",
        "city": "Karachi",
        "note": f"Result based on query: {query}"
    }



# -------------------------
# Dynamic instructions
# -------------------------
def special_prompt(context: RunContextWrapper[UserContext], agent: Agent[UserContext]):
    return (
        f"You are a helpful assistant specialized in math.\n"
        f"User: {context.context.username}\n"
        f"Agent: {agent.name}\n\n"
        "If the user asks about their area, location, or finding someone nearby, "
        "ALWAYS call the `search` tool first. Then, use the tool's returned values "
        "(country and city) in your final answer. Do not say you cannot access location."
    )



# -------------------------
# Main Runner
# -------------------------
def main():
    user_context = UserContext(username="Nehal")

    math_agent = Agent(
        name="Genius",
        instructions=special_prompt,
        model=model,
        tools=[search],
    )

    result = Runner.run_sync(
        starting_agent=math_agent,
        input="search for the best tutor in my area.",
        context=user_context,
    )

    print("\n--- Final Output ---")
    print(result.final_output)


if __name__ == "__main__":
    main()
