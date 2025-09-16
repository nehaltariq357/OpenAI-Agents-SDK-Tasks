from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field
from typing_extensions import Annotated

# Generic type variable
T = TypeVar("T")

# Generic container model
class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int

# Inner model with constraint
class Item(BaseModel):
    name: Annotated[str, Field(min_length=2)]

# Example usage
p = Page[Item](
    items=[{"name": "ab"}],
    total=1
)

print(p.model_dump())
