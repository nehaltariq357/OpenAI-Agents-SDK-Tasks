
from agents import Agent,Runner,SQLiteSession

class MyAgentWithMemory:

    def __init__(self,session_name = "default_session"):
        self.agent = Agent(
            name = "MYAgent",
            instructions="You are a friendly assistant who remembers conversation."
        )
        # create session
        self.session = SQLiteSession(session_name,"my_agent_memory.db")

    def ask(self,message):
        # Run the agent synchronously
        result = Runner.run_sync(
            starting_agent=self.agent,
            input=message,
            session=self.session
        )
        return result.final_output
    
bot = MyAgentWithMemory()
print("User: Hi! My name is Alex")
print("Bot:", bot.ask("Hi! My name is Alex"))

print("User: What's my name?")
print("Bot:", bot.ask("What's my name?"))