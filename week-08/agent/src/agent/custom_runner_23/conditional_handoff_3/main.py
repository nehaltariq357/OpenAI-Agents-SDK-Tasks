import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper, handoff
from pydantic import BaseModel
from rich import print

load_dotenv(find_dotenv())

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# Setup LLM
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

# Context model
class MyContext(BaseModel):
    subscription_tier: str
    has_permission: bool = False


# Expert Agent
expert_agent = Agent(
    name="MathExpert",
    instructions="You are a math expert. Solve all math-related queries precisely.",
    model=model,
)

# Main Agent
main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Delegate math queries if allowed.",
    model=model,
)

# Add handoff to main agent
main_agent.handoffs = [
    handoff(
        expert_agent,
        is_enabled=lambda ctx, agent: ctx.context.has_permission,
    )
]


def main():
    # Case 1: User WITHOUT permission
    free_ctx = MyContext(subscription_tier="free", has_permission=False)
    result1 = Runner.run_sync(
        main_agent, input="Solve 25 * 4", context=free_ctx
    )
    print("[red]Free User Result:", result1.final_output)

    # Case 2: User WITH permission
    premium_ctx = MyContext(subscription_tier="premium", has_permission=True)
    result2 = Runner.run_sync(
        main_agent, input="Solve 25 * 4", context=premium_ctx
    )
    print("[green]Premium User Result:", result2.final_output)


if __name__ == "__main__":
    main()
