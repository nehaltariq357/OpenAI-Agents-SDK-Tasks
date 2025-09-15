from pydantic.dataclasses import dataclass

@dataclass
class Uservalidated:
    name:str
    age:int

u = Uservalidated(name="Ali", age="20")  # ✔ "20" --> int(20) 
print(u)  # UserValidated(name='Ali', age=20)

bad = Uservalidated(name="Ali", age="twenty")  # ❌ ValidationError