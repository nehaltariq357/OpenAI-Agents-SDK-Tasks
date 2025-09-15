from pydantic import BaseModel,Field,ValidationError
from typing_extensions import Annotated
from rich import print

class User(BaseModel):

    username:str =Field(..., min_length=3,max_length=15)
    age:int = Field(..., ge=18)
    email:str = Field(..., pattern=r'^\S+@\S+\.\S+$', description="Valid email address")
    hobbies:list[Annotated[str,Field(...,min_length=2)]] = Field(min_length=1)

try:
    u1 = User(username="Alice",age=40,email="abc@gmail.com",hobbies=["reading","writing"])

    print(u1.model_dump())
except ValidationError as e:
    print("validation error: ",e)