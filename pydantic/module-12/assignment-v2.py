from pydantic import BaseModel, field_validator

class Product(BaseModel):
    title: str
    price: float

    @field_validator("title")
    def check_title(cls, v):
        if len(v) < 3:
            raise ValueError("Title too short")
        return v

    @field_validator("price")
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v

p = Product(title="python", price=10)
print(p.model_dump())
print(p.model_dump_json())
