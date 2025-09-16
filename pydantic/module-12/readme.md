># Theory — Migration Checklist

| pydantic v1 | pydantic v2 |
|:-----------:|:-----------:|
|model.dict() |model.model_dump()|
|model.json()|model.model_dump_json()|
|schema()|model_json_schema()|
|@validator|@field_validator (for fields), @model_validator (for whole model)|
|Dataclasses validation|Use TypeAdapter to validate / dump / schema

***v2 also introduces faster core (Rust, pydantic-core) and stricter typing.***

### Old Pydantic v1 code

```python
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str
    age: int

    @validator("age")
    def check_age(cls, v):
        if v < 18:
            raise ValueError("Must be at least 18")
        return v

u = User(name="Ali", age=20)
print(u.dict())       # v1 style
print(u.json())       # v1 style
print(User.schema())  # v1 style

```

### Updated Pydantic v2 code
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def check_age(cls, v):
        if v < 18:
            raise ValueError("Must be at least 18")
        return v

u = User(name="Ali", age=20)
print(u.model_dump())         # ✅ replaces dict()
print(u.model_dump_json())    # ✅ replaces json()
print(User.model_json_schema())  # ✅ replaces schema()

```

