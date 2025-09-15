from pydantic import BaseModel, field_validator, model_validator
from rich import print
class User(BaseModel):
    username: str
    age: int

    @model_validator(mode="before")
    def before_model(cls, data):
        print("1. before model:", data)
        return data

    @field_validator("username", mode="before")
    def before_username(cls, v):
        print("2. before username:", v, type(v))
        return v

    @field_validator("age", mode="before")
    def before_age(cls, v):
        print("3. before age:", v, type(v))
        return v

    @field_validator("age", mode="after")
    def after_age(cls, v):
        print("4. after age:", v, type(v))
        return v

    @model_validator(mode="after")
    def after_model(cls, model):
        print("5. after model:", model)
        return model

# Run
u = User(username=" Ali ", age="25")
