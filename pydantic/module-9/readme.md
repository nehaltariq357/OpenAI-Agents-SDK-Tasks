># Module 9 — Generics, Annotated, and constrained types

## 1. Generics

- Sometimes we want to create a container model that works for all types.
- Sample: A page[T] model that can handle any number of `Items`, `User`, and `product` pages.
- `T = TypeVar("T")` --> to define generic type.
- power for resuability.

## 2. Annotated

- Recommended way to apply constraints to pydantic v2.
- Writing `Annotated[<type>, Field(...)]` will bury columns + roles in the same place.

## Example:

```python
from typing_extensions import Annotated
from pydantic import Field

Age = Annotated[int, Field(ge=18)]

```
- `Age` is int and always greater than 18

## 3. Constrained Types

- in pydantic v1 `conint, constr` used, (eg, conint(ge=18)).
- in pydantic v2 `Annotated[int, Field(...)]` is recommended to use.
- this is more readable and flexible.

