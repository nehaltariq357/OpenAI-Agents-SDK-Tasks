import os
import asyncio
from agents import Agent, RunContextWrapper, Runner, function_tool,AsyncOpenAI,OpenAIChatCompletionsModel,set_tracing_disabled
from pydantic import BaseModel
import rich
from dotenv import load_dotenv
set_tracing_disabled(disabled=True)
load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")

# ------------------- CONTEXT MODELS -------------------
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)
class BankAccount(BaseModel):
    account_number: str
    customer_name: str
    account_balance: float
    account_type: str

class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int

class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool


# ------------------- LOCAL CONTEXT DATA -------------------

bank_account = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="savings"
)

student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)

library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)


# ------------------- TOOLS -------------------

@function_tool
def get_bank_account(wrapper: RunContextWrapper[BankAccount]):
    return f"🏦 Account {wrapper.context.account_number} belongs to {wrapper.context.customer_name}, Balance: {wrapper.context.account_balance}, Type: {wrapper.context.account_type}"

@function_tool
def get_student_profile(wrapper: RunContextWrapper[StudentProfile]):
    return f"🎓 Student {wrapper.context.student_name} (ID: {wrapper.context.student_id}) is in semester {wrapper.context.current_semester} with {wrapper.context.total_courses} courses."

@function_tool
def get_library_book(wrapper: RunContextWrapper[LibraryBook]):
    status = "available ✅" if wrapper.context.is_available else "not available ❌"
    return f"📚 Book '{wrapper.context.book_title}' by {wrapper.context.author_name} is {status}."


# ------------------- AGENTS -------------------

bank_agent = Agent(
    name="Bank Agent",
    instructions="You are a helpful bank assistant. Always use the tool to fetch bank account details.",
    tools=[get_bank_account],
    model=llm_model
)

student_agent = Agent(
    name="Student Agent",
    instructions="You are a helpful student portal assistant. Always use the tool to fetch student profile.",
    tools=[get_student_profile],
    model=llm_model
)

library_agent = Agent(
    name="Library Agent",
    instructions="You are a helpful librarian. Always use the tool to fetch book details.",
    tools=[get_library_book],
    model=llm_model
)


# ------------------- MAIN -------------------

async def main():
    # Bank Context
    bank_result = await Runner.run(
        bank_agent,
        "Can you show me my bank account details?",
        context=bank_account
    )
    rich.print(bank_result.final_output)

    # Student Context
    student_result = await Runner.run(
        student_agent,
        "Give me my student profile summary.",
        context=student
    )
    rich.print(student_result.final_output)

    # Library Context
    book_result = await Runner.run(
        library_agent,
        "Tell me about the book in the library.",
        context=library_book
    )
    rich.print(book_result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
