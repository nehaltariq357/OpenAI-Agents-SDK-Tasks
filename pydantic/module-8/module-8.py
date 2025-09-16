from datetime import datetime
from pydantic import BaseModel, field_serializer

class Event(BaseModel):
    name: str
    time: datetime

    # Custom serializer for time
    @field_serializer("time")
    def serialize_time(self, v: datetime):
        return v.isoformat()   # datetime → ISO string

# Model instance
e = Event(name="Launch", time="2025-01-01T10:00:00")

# Default dict dump
print(e.model_dump())      
# {'name': 'Launch', 'time': datetime.datetime(2025, 1, 1, 10, 0)}

# JSON dump (custom serialization applied)
print(e.model_dump_json())  
# {"name": "Launch", "time": "2025-01-01T10:00:00"}
