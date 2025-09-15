># Module 5 — Pydantic Dataclasses

>## a. Normal Python `@dataclass`

- python have built-in dacorator called `@dataclass`.
- It makes class simple data container.
- no need to write this `__init__, __repr__, __eq__,`.
- but there is not type validation in this. 
  - means if field has `int` declared, then you pass `abc` it will accept without error.
### Example:

```python
from dataclasses import dataclass

@dataclass
class User:
    name:str
    age:int

u = User(name="Ali",age="fifty") # incorrect input, but there will be no error
print(u)  # User(name='Ali', age='twenty')
```

> # b. Pydantic `@dataclass`
- pydantic gives a decorator called `@pydantic.dataclasses.dataclass`.
- it has same dataclass behavoir (lightweight object, auto `__init__` etc.).
- but it also adds type validation and conversion.
- the benefits of this is that you can use the simplicity of dataclass along with pydantic's validation.
  
### Example:

```python
from pydantic.dataclasses import dataclass

@dataclass
class UserValidated:
    name:str
    age:int

u = UserValidated(name="Ali", age="20")  # ✔ "20" --> int(20) 
print(u)  # UserValidated(name='Ali', age=20)

bad = UserValidated(name="Ali", age="twenty")  # ❌ ValidationError
```

># c. TypeAdapter
- if you want to make dataclass object(with validation) from dict, then you should use `TypeAdapter`.
- This programmatically checks the data and can also generate JSON Schema.

># d. __post_init__
- dataclasses have special method `__post_init__`.
- this runs when the object is created.
- in pydantic v2, it runs after validation.
- This means that first the fields are validated, then your custom logic runs.
  
### Example:

```python
from pydantic.dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")

```