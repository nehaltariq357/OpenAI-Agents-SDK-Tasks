># Module 6 — TypeAdapter (validate ANY type)

- `TypeAdapter` is a universal validator, which is used to validate and serialize any Python type (whether it is a BaseModel, dataclass, list[int], TypedDict, or a custom type).

># Features
1. `validate_python(input)`
    - validate or coerce input (if '1' is given and int is expected then it will convert).
2. `dump_json(obj)`
    - convert object into JSON string.
    - in pydantic v2 it return bytes(so need to decode)
3. `json_schema()`
    - A schema generates that describes the structure of a type (for documentation or validation).
4. Performance Tip
    - If you need to use the same TypeAdapter repeatedly, then cache it, because computing `json_schema()` is costly.
