> # Validator (Field & Model)

> ### Problem:
- by default `BaseModel` check only types.
>### Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

u = User(name="Ali",age="50") # ✅ string "20" int ban gaya
u = User(name="Ali", age=-5)     # ❌ Negative age bhi allowed hogi (galat hai)

```

- means type is correct, logical rule may be incorrect.
- here comes `validators`

>## Validator's Types

### 1. `@field_validator("field")` 
- make for only one field
- ### Example:
    - check minimum length of `password`
    - strip spaces in `username`

- ### Modes:
- before type convresion --> `mode="before"`
- after type conversion --> default `(after)`

### 2. `@model_validator(mode="before"|"after")`

- make rules on models/all fieldes
- useful to check 2 or more fields relations
  - Example: `end_date > start_date`
  - Example: `password != username`
  
  ---

# Validation Order

1. `model_validator(mode="before")` → raw data
2. `field_validator(..., mode="before")` → raw value of every field
3. ## Type conversion (str → int, float, etc.)

4. `field_validator(..., mode="after")` → converted values
5. `model_validator(mode="after")` → final object