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
class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: int
    gpa: Optional[float] = None

class Experience(BaseModel):
    position: str
    company: str
    start_year: int
    end_year: Optional[int] = None  # None if current job
    responsibilities: List[str]

class Resume(BaseModel):
    full_name: str
    email: str
    phone: str
    summary: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    languages: List[str]




agent = Agent(
    name="ResumeParser",
    instructions="Extract structured information from resume text.",
    model=model,
    output_type=Resume   # This is the magic!
)

def main():
    sample_resume = """
    John Smith
    Email: john.smith@email.com, Phone: (555) 123-4567

    Professional Summary:
    Experienced software developer with 5 years in web development and team leadership.

    Education:
    - Bachelor of Computer Science, MIT, 2018, GPA: 3.8
    - Master of Software Engineering, Stanford, 2020

    Experience:
    - Senior Developer at Google (2020-present): Led team of 5 developers, implemented microservices architecture
    - Junior Developer at Startup Inc (2018-2020): Built React applications, maintained CI/CD pipelines

    Skills: Python, JavaScript, React, Docker, Kubernetes
    Languages: English (native), Spanish (conversational), French (basic)
    """


    # Test it
    result = Runner.run_sync(
        starting_agent=agent,
        input=sample_resume,
    )


    # Now you get perfect structured data!
    print("=== Parsed Resume ===")
    print(f"Name: {result.final_output.full_name}")
    print(f"Email: {result.final_output.email}")
    print(f"Phone: {result.final_output.phone}")
    print(f"Summary: {result.final_output.summary}") 

    print("\nEducation:")
    for edu in result.final_output.education:
        gap_str = f"GPA: {edu.gpa}"  if edu.gpa else ""
        print(f"  • {edu.degree} from {edu.institution} ({edu.graduation_year})-{gap_str}")

    print("\nExperience:")
    for exp in result.final_output.experience:
        end_year = exp.end_year if exp.end_year else "present"
        print(f"  • {exp.position} at {exp.company} ({exp.start_year}-{end_year})")
        
    print("\Responsibilities:")
    for resp in exp.responsibilities:
        print(f"    - {resp}")

    print(f"\nSkills: {', '.join(result.final_output.skills)}")
    print(f"Languages: {', '.join(result.final_output.languages)}")

if __name__ == "__main__":
    main()






