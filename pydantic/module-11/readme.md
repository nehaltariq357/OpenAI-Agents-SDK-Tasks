># Module 11 — Agents & output_type (LLM integration)

- LLMs (ChatGPT, Claude, Gemini, etc.) provide free-text/unstructured output.
- if you want to structured output (jaise JSON ya Python object),--> you need to specify schema.

### Advantage of pydantic

- You create a `BaseModel` or @`DataClass` for the schema.
- Telling the agent that his `output_type` is this model.
- when the LLM respose --> pydantic automatically validate + coerce.
- if incorrect format --> validation error.
  
***This way you always get clean structured data (not messy text).***

## Practical (pseudo example)

```python
from dataclasses import dataclass

# Step 1:define Schema  
@dataclass
class Book:
    title: str
    author: str
    year: int

# Step 2:provide schema to Agent 
# (Pseudo code, SDK-specific)
# agent = Agent(
#     instructions="Extract book details from this paragraph",
#     output_type=Book
# )

# Step 3: Agar agent ne kuch bhi return kiya:
# {"title": "1984", "author": "George Orwell", "year": "1949"}
# To ye automatic convert + validate hoga:
# Book(title="1984", author="George Orwell", year=1949)

```

