from pydantic import TypeAdapter
from rich import print
from pydantic.dataclasses import dataclass
@dataclass
class Student:
    name: str
    age:int

TA = TypeAdapter(Student)
evt = TA.validate_python({
    "name":"Ali",
    "age":"55"
})
print(evt)