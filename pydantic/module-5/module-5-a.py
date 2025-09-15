from dataclasses import dataclass
@dataclass
class User:
    name:str
    age:int

u = User(name="Ali",age="fifty") # incorrect input, but there will be no error
print(u)  # User(name='Ali', age='twenty')