import os
from agents import Agent,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
from typing import Optional,List

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

# Define your data structure
class ActionItem(BaseModel):
    task: str
    assignee: str
    due_date: Optional[str] = None
    priority: str = "medium"

class Decision(BaseModel):
    topic: str
    decision: str
    rationale: Optional[str] = None

class MeetingMinutes(BaseModel):
    meeting_title: str
    date: str
    attendees: List[str]
    agenda_items: List[str]
    key_decisions: List[Decision]
    action_items: List[ActionItem]
    next_meeting_date: Optional[str] = None
    meeting_duration_minutes: int




agent = Agent(
    name="MeetingSecretary",
    instructions="""Extract structured meeting minutes from meeting transcripts.
    Identify all key decisions, action items, and important details.""",
    model=model,
    output_type=MeetingMinutes   # This is the magic!
)

def main():
    # Test it
    meeting_transcript = """
Marketing Strategy Meeting - January 15, 2024
Attendees: Sarah (Marketing Manager), John (Product Manager), Lisa (Designer), Mike (Developer)
Duration: 90 minutes

Agenda:
1. Q1 Campaign Review
2. New Product Launch Strategy  
3. Budget Allocation
4. Social Media Strategy

Key Decisions:
- Approved $50K budget for Q1 digital campaigns based on strong ROI data
- Decided to launch new product in March instead of February for better market timing
- Will focus social media efforts on Instagram and TikTok for younger demographics

Action Items:
- Sarah to create campaign timeline by January 20th (high priority)
- John to finalize product features by January 25th
- Lisa to design landing page mockups by January 22nd
- Mike to review technical requirements by January 30th

Next meeting: January 29, 2024
"""
    result = Runner.run_sync(
        starting_agent=agent,
        input=meeting_transcript,
    )


        # Now you get perfect structured data!
    print("\n=== Meeting Minutes ===\n")
    print(f"\nMeeting Minutes: {result.final_output}")
    print(f"\nMeeting Title: {result.final_output.meeting_title}")
    print(f"\nMeeting Date: {result.final_output.date}")
    print(f"\nMeeting Attendees: {result.final_output.attendees}")
    print(f"\nMeeting Agenda Items: {result.final_output.agenda_items}")
    print(f"\nMeeting Key Decisions: {result.final_output.key_decisions}")
    print(f"\nMeeting Action Items: {result.final_output.action_items}")
    print(f"\nMeeting Next Meeting Date: {result.final_output.next_meeting_date}")
    print(f"\nMeeting meeting Duration Minutes: {result.final_output.meeting_duration_minutes}")



if __name__ == "__main__":
    main()






