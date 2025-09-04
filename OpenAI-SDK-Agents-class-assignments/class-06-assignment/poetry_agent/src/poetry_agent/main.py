import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner, trace
from dotenv import load_dotenv
import asyncio
import rich

load_dotenv()

# ONLY FOR TRACING
openai_key = os.getenv("OPENAI_API_KEY", "")
os.environ["OPENAI_API_KEY"] = openai_key  

# gemini api key , for model calling
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash"
)

# === Poet Agent ===
poet_agent = Agent(
    name="Poet Agent",
    instructions="""
    You are a creative poet. Write a short 2-stanza poem 
    based on the user's request. Keep it clear and creative.
    """,
    model=llm_model
)

# === Analyst Agents ===
lyric_agent = Agent(
    name="Lyric Analyst",
    instructions="""
    You are a Lyric Poetry Analyst.
    If the poem expresses personal feelings/emotions,
    explain how it is a lyric poem.
    """,
    model=llm_model
)

narrative_agent = Agent(
    name="Narrative Analyst",
    instructions="""
    You are a Narrative Poetry Analyst.
    If the poem tells a story with characters/events,
    explain how it is narrative poetry.
    """,
    model=llm_model
)

dramatic_agent = Agent(
    name="Dramatic Analyst",
    instructions="""
    You are a Dramatic Poetry Analyst.
    If the poem feels like performance/theatre/monologue,
    explain how it is dramatic poetry.
    """,
    model=llm_model
)

# === Triage / Orchestrator Agent ===
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a triage/orchestrator.
    Your job is NOT to answer directly.
    Instead:
    - If input or generated poem is about feelings/thoughts → handoff to Lyric Analyst.
    - If it's storytelling with characters/events → handoff to Narrative Analyst.
    - If it's performative/theatre-like → handoff to Dramatic Analyst.
    
    Always use a handoff to the correct analyst agent instead of answering yourself.
    """,
    model=llm_model,
    handoffs=[poet_agent, lyric_agent, narrative_agent, dramatic_agent]
)

# === MAIN (async) ===
async def main():
    result = await Runner.run(
        starting_agent=triage_agent,
        # input="Write a poem about heartbreak and loneliness",  # → Lyric
        # input=" Write a poem telling the story of a brave knight who saves a village",  # → Narrative
        input= "Write a poem like a dramatic monologue where a king speaks to his people"  # → Dramatic
    )
    print("\n--- Final Analyst Response ---\n")
    print("agent name: ",result.last_agent.name)
    print(result.final_output)

asyncio.run(main())
