> # Module 10 — TypedDict & dict-like schemas

- Sometimes we don't need objects (basemodel / dataclasses), but rather a dictionary-like schema.
- In python `TypedDict` is used for this, --> dict strcuture type hint schema.
- but normal `TypedDict` only provide type hint, not validation.
- if you also want validation, ---> use pydantic's `TypeAdapter`
  - `validate_python()` --> It will check the dict and convert the proper types.
  - `json_schema()` --> make schema.
  - `dump_json()` --> generate JSON output.
  