from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
from rich import print

@dataclass 
class Movie:
    title:str
    year:int

TA = TypeAdapter(Movie)
evt = TA.validate_python({
    "title":"Movie-1",
    "year":"2020"
})

print(evt)
print(TA.json_schema())