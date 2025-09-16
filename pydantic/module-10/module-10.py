from typing import TypedDict
from pydantic import TypeAdapter
from rich import print

class RawUser(TypedDict):
    id: int
    name: str

ta = TypeAdapter(RawUser)

# input me id string hai, wo int me convert ho jayegi
user = ta.validate_python({"id": "1", "name": "Ali"})
print(user)                # {'id': 1, 'name': 'Ali'}

# schema print karna
print(ta.json_schema())    

# json dump
print(ta.dump_json(user))  
