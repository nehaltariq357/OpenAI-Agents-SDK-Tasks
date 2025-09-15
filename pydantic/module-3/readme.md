> # 1. What is Field(...)?
- We make fields (name: str, price: float) in BaseModel.
- Adds extra rules/metadata in fields, we use `Field(...)`
> Rules:
- works for validations (e.g., min_length=2, ge=0).
- And show in schema (OpenAPI, JSON Schema, docs).

># 2. Common Constraints
- `min_length` --> for minimum characters.
- `max_length` --> for maximum characters.
- `ge` --> greater than or equal (>=).
- `le` --> less than or equal (<=).
- `pattern` --> pattern match.
- `description` --> explanation for schema/documentation.
- `examples` --> sample data for docs.

># 3. Uses of Annotated (v2 style)
- we use `Annotated` to add constraints in lists/nested items.
> Example:

```python
list[Annotated[str, Field(min_length=2)]]
``` 
>Note:
- ek list jisme sirf aise strings honge jinki minimum length 2 hai.