># serialization

- convert the model in output format.
- sometime you need special formatting in API response.
  
### Example

- convert `datetime` in ISO string.
- masking password or sensitive data.
- custom representation.

### there are two decorators in pydantic v2

>## 1. `@field_serializer("field_name")`

- customize the specific field output
- The input remains normal, only the output `(.model_dump(), .model_dump_json())` is formatted.

>## 2. `@model_serializer(mode="wrap")`

- If you want to customize the output of the entire model, you can do so.
- Sample: Creating a custom JSON structure of multiple fields at once.