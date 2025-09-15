
from dataclasses import field
from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
from rich import print
@dataclass
class Event:
    title: str
    attendees: list[str] = field(default_factory=list)
    duration_min: int = 0

# TypeAdapter se dict validate karke Event object banate hain
TA = TypeAdapter(Event)

evt = TA.validate_python({
    "title": "Standup",
    "attendees": ["Ali", "Sara"],
    "duration_min": "15"   # str ko int me convert karega
})

print(evt)                # Event(title='Standup', attendees=['Ali','Sara'], duration_min=15)
print(TA.json_schema())   # Schema print karega (types aur constraints dikhayega)
