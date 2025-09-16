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