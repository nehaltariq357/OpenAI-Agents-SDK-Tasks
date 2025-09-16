from pydantic import BaseModel,Field
from typing import Generic,TypeVar,List
from typing_extensions import Annotated
from rich import print

T = TypeVar("T")

class Catalog(BaseModel,Generic[T]):
    products:List[T]
    count:int

class Product(BaseModel):
    title:Annotated[str,Field(...,min_length=3)]
    price:Annotated[float,Field(...,ge=1)]


try:
    catalog_invalid = Catalog[Product](
        products=[
            {"title": "AB111", "price": 500},  
            {"title": "Book", "price": 5.2}  
        ],
        count=2
    )
    print(catalog_invalid.model_dump())
except Exception as e:
    print("❌ Validation Error:")
    print(e)
