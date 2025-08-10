from dataclasses import dataclass
import os
from agents import Agent,AsyncOpenAI,OpenAIChatCompletionsModel,RunConfig,Runner,RunContextWrapper
from dotenv import load_dotenv
load_dotenv() # load env file
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
    raise ValueError("GEMINI_API_KEY not set in .env")

Gemini_client = AsyncOpenAI(
    api_key=GEMINI_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)

model= OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=Gemini_client
)

config = RunConfig(
    model=model,
    model_provider=Gemini_client,
    tracing_disabled=True
)

@dataclass
class UserInfo:
    username:str
    email:str
    mode:str = "shakespeare" # default mode

# dynamic instrctions

def dynamic_instruction(wrapper:RunContextWrapper,agent:Agent):
    """Return system-style instructions depending on wrapper.context.mode.wrapper.context is the UserInfo instance we passed to Runner.run_sync(...)"""
    
    # safety: if now context is provided
    if not getattr(wrapper,"context",None):
        return "You are a helpful assistant. Speak normally."

    # getting mode
    mode = getattr(wrapper.context,"mode","shakespeare")
    # getting user name 
    user_name = getattr(wrapper.context,"username","user")
    # getting user email
    user_email = getattr(wrapper.context,"email","no email found")

    match mode:
        case "shakespeare":
            return (
                f"You are William Shakespeare reincarnated. Speak in Early Modern English, "
                f"use poetic phrasing and archaic words. Address the user as '{user_name}' politely.{user_email}"
            )
        case "genz":
            return (
                f"You are a Gen Z influencer. Use casual slang, contractions, emojis, short sentences, "
                f"and a friendly tone. Address the user as '{user_name}' casually.{user_email}"
            )
        case _:
            return f"You are a helpful assistant. Address {user_name} politely.{user_email}"


def main():
    # this is context-initial
    user = UserInfo(
        username="Nehal",
        email = "xyz@gmail.com",
        mode = "shakespeare"
    )
    while True:
        user_text = input("You: ").strip().lower()

        # skips if input is empty
        if not user_text:
            continue

        # exit command
        if user_text in ("exit","quit","bye"):
            print("Bye!")
            break

        # switch mode command
        # starts with switch, then genz or shakespeare
        if user_text.startswith("switch"):
            new_mode = user_text.split(maxsplit=1)[1] # selects second word like genz or shakespeare
            if new_mode in ("shakespeare","genz"):
                user.mode = new_mode
                print(f"Mode switched to: {user.mode}")
            else:
                print("Unknown mode. Available ['shakespeare' or 'genz']")
            continue # it means, after change mode, again user input run, not agent reply
        agent = Agent(
            name="style_switcher",
            instructions=dynamic_instruction,
            model=model
        )

        result = Runner.run_sync(
            starting_agent=agent,
            input=user_text,
            run_config=config,
            context=user
        )

        print("Bot",result.final_output)
        print("*"*40)