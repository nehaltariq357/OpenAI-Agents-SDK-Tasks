from agents import Agent,Runner,set_tracing_disabled

from dotenv import load_dotenv
import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
set_tracing_disabled(disabled=True)
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

agent = Agent(
    name="Translator agent",
    instructions =( 
        """
        You are a translation agent. 
        - Task: Translate the given text into the target language requested by the user.  
        - If the target language is not mentioned, respond with: "Which language do you want me to translate into?"  
        - Always correct grammar and spelling in the translated text.  
        - Output must contain only the translated sentence (no extra notes or explanations).  
        """
),
    model=model
)

def main():
    queries= [
        "he is going to school, translate this into urdu",
        "translate 'I love programming' into french",
        "translate 'the weather is very hot today' into arabic",
        "translate 'we are learning artificial intelligence' into chinese",
        "this is a test sentence"  # no language given
    ]
    for query in queries:
        print(f"\nUser Input: {query}")
        result = Runner.run_sync(
            starting_agent=agent,
            input=query
        )

        print(f"Translation: {result.final_output}")