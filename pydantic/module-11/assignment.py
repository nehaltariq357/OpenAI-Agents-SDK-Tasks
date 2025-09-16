from dataclasses import dataclass
from pydantic import TypeAdapter
@dataclass
class User:
    name: str
    age: int
    email: str


output_type = {"name": "Ali", "age": "25", "email": "ali@example.com"}

ta = TypeAdapter(User)

u = ta.validate_python(output_type)

print(u)
print(ta.dump_json(u))