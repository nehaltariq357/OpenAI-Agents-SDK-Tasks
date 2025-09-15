from pydantic import BaseModel
from rich import print

# Nested Model
class Address(BaseModel):
    city: str
    postcode: str

class User(BaseModel):
    name: str
    address: Address   # nested model

# Validate dict input
u = User.model_validate({
    "name": "Ali",
    "address": {
        "city": "Karachi",
        "postcode": "12345"
    }
})

# Dump output
print(u.model_dump())
