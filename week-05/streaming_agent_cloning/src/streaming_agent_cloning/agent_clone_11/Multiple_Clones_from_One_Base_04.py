import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,ModelSettings,function_tool
from dotenv import load_dotenv
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

def main():

# Base agent with one tool 
    base_agent = Agent(
    name="BaseAssistant",
    instructions="you are helpful assistant",
    model=model,
    model_settings=ModelSettings(temperature=0.7)
)
# Create multiple specialized variants
    agents={
        "creative": base_agent.clone(
            name = "CreativeWriter",
            instructions = "You are a creative writer. Use vivid language.",
            model_settings=ModelSettings(temperature=0.9)
        ),
        "Precise": base_agent.clone(
            name = "PreciseAssistant",
            instructions = "You are a precise assistant. Be accurate and concise.",
            model_settings=ModelSettings(temperature=0.1)
        ),
        "Friendly": base_agent.clone(
            name = "FriendlyAssistant",
            instructions = "You are a very friendly assistant. Be warm and encouraging.",
        ),
        "Professional": base_agent.clone(
            name = "ProfessionalAssistant",
            instructions = "You are a professional assistant. Be formal and business-like.",
        ),
    }

    # Test all variants
    query = "Tell me about artificial intelligence."

    for name,agent in agents.items():
        result = Runner.run_sync(
            starting_agent=agent,
            input=query
        )
        print(f"\n{name} Agent:")
        print(result.final_output[:100] +"....")