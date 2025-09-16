from pydantic import BaseModel,field_serializer
from rich import print
class User(BaseModel):
    username:str
    password:str

    @field_serializer("password")
    def pw_mask(self,v):
        return "****"

u = User(username="Ali",password="abc13")

print(u.model_dump())       
print(u.model_dump_json())   