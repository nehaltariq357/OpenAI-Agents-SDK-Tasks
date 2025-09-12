from pydantic import BaseModel, ValidationError

class Book(BaseModel):
    isbn: str
    title: str
    price: float
    pages: int

data = {
    "isbn": "111",
    "title": "the python",
    "price": "20.5",   # FIXED: removed $
    "pages": "200"
}

try:
    # Step 1: Validate input dict
    b = Book.model_validate(data)

    # Step 2: Convert to dict
    dict_data = b.model_dump()

    # Step 3: Convert to JSON string
    json_str = b.model_dump_json()

    # Step 4: Generate JSON Schema
    json_schema = Book.model_json_schema()

    print("Instance:", b)
    print("As dict:", dict_data)
    print("As JSON:", json_str)
    print("JSON Schema:", json_schema)

except ValidationError as e:
    print("Validation Error:", e)
