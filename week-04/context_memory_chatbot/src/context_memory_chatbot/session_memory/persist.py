
import os
from dotenv import load_dotenv
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled,Runner,SQLiteSession
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

set_tracing_disabled(disabled=True)
external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client,
)

def main():
    agent = Agent(
        name="Assistant",
        instructions="you are helpful assistant",
        model=model
    )

    # Temporary memory (lost when program ends)

    temp_session = SQLiteSession("temp_conversation")

    # Persistent memory (saved to file)
    persistent_session = SQLiteSession(session_id="user123",db_path="conversations.db")

    # Use temporary session
    result1 = Runner.run_sync(
        starting_agent=agent,
        input="Remember: my favorite color is blue",
        session=temp_session
    )
    

    # Use persistent session
    result2 = Runner.run_sync(
        starting_agent=agent,
        input="Remember: my favorite color is blue",
        session=persistent_session
    )

    
    print("Both sessions now remember your favorite color!")
    print("But only the persistent session will remember after restarting the program.")