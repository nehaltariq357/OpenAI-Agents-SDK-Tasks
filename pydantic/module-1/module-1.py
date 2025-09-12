#  Module 1 — Basic idea: Type hints + runtime validation
#  Theory (simple)
#  Python me type hints sirf hints hote hain. Pydantic un hints ko runtime pe use 
# karke:
#  validate karta hai (type match),
#  coerce(force) karta hai jab possible ho ("25" → 25),
#  throw karta hai helpful errors agar invalid ho.
#  Ye bahut useful hai jab data bahar se aata hai (API, user input, LLMs, config 
# files).

# Practical:

from pydantic import BaseModel

# Direct Instantiation
class User(BaseModel):
    name:str
    age:int

u = User(name="Ali",age="50")   # "50" coerced to int
print(u)  #----->  # User(name='Ali', age=50)

