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
