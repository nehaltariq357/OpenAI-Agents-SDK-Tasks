# # 1. BaseModel kya hai?
# BaseModel pydantic ka main class hai.
# Isse hum apne custom data models banate hain.
# Har field ke liye type define karte hain (e.g., int, str, float).
# input dete ho to pydantic automatic validation + type conversion karta hai.

# 2. Important Methods of BaseModel

# a. model_validate(data):
# works--> raw inputs(dict,json,etc.) ko check karke valid instance banata ha.
# Extra benefit: Agar types thodi mismatched hain (e.g., "101" string diya int ke jagah), to pydantic usko convert karne ki koshish karega.

from pydantic import BaseModel
from rich import print
class Student(BaseModel):
    id:int
    name:str
    gpa:float

# Using model_validate
# Raw data (notice: id and gpa are strings)
data = {"id": "101", "name": "Sara", "gpa": "3.5"}


# s = Student.model_validate(data)
# print(s)  # --->  id=101 name='Sara' gpa=3.5

# **************************************************************************************

# b. module_dump():
# works---->model ko python dict me convert krta ha.
# Ye mostly useful hai jab tum apna model JSON me convert karna chahte ho, ya database/other API me bhejna ho.

class Student(BaseModel):
    id:int
    name:str
    gpa:float

data ={"id": "101", "name": "Sara", "gpa": "3.5"}


s  = Student.model_validate(data)
# print(s.model_dump())  # ----> {'id': 101, 'name': 'Sara', 'gpa': 3.5}

# **************************************************************************************


# c.modul_dump_json():
# works-----> converts model, into json string
# use when working with json API 

class Student(BaseModel):
    id:int
    name:str
    gpa:float
    
user = Student(id="55",name="Ali",gpa="3.5")
u = user.model_validate(user)
# print(u.model_dump_json())  #  ----> {"id":55,"name":"Ali","gpa":3.5}

# **************************************************************************************

# d. model_json_schema()
# works----> provide json schema to model.
# JSON Schema ek formal definition hota hai jo batata hai model me kaunse fields hain, unke types kya hain, aur rules kya hain.
# Ye APIs (like FastAPI, OpenAPI docs) ke liye useful hai.

class Student(BaseModel):
    id:int
    name:str
    gpa:float

user = Student(id="55",name="Ali",gpa="3.5")
u = user.model_validate(user)
# print(u.model_json_schema())

# output:
{
    'properties': {'id': {'title': 'Id', 'type': 'integer'}, 'name': {'title': 'Name', 'type': 'string'}, 'gpa': {'title': 'Gpa', 'type': 'number'}},
    'required': ['id', 'name', 'gpa'],
    'title': 'Student',
    'type': 'object'
}

# **************************************************************************************

# e. model_config:
# works--> define class level options.
# Example: Agar tum chahte ho ke extra fields allow na ho, to extra="forbid" use kar sakte ho.

class Student(BaseModel):
    id: int
    name: str
    gpa: float

    class Config:
        extra = "forbid"

# Ab agar extra field diya to error aayega:
try:
    s = Student.model_validate({"id": 101, "name": "Sara", "gpa": 3.5, "age": 20})
except Exception as e:
    print("Error:", e) # --> age Error: 1 validation error for Student

