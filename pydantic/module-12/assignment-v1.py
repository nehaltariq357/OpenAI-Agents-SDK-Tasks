from pydantic import BaseModel, validator

class Product(BaseModel):
    title: str
    price: float

    @validator("title")
    def check_title(cls, v):
        if len(v) < 3:
            raise ValueError("Title too short")
        return v

    @validator("price")
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v

p = Product(title="AB", price=10)
print(p.dict())
print(p.json())
