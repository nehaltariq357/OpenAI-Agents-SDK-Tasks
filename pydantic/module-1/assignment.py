
from pydantic import BaseModel

class Person(BaseModel):
    name:str
    height:float



try:
    # p = Person(name="Ali",height="170.5") # ---> should work
    p = Person(name="Ali",height="one-seventy") # should raise error
    print(p)
except:
    print("Error")