
from pydantic import TypeAdapter

from rich import print

lst = TypeAdapter(list[int])


# Example 1: Validation with coercion

print(lst.validate_python(["1",2,3,"4"])) # --> [1, 2, 3, 4]

# Example 2: Dump JSON

json_bytes = lst.dump_json([1, 2, 3])
print(json_bytes.decode()) # --> [1,2,3]

# Example 3: JSON Schema
print(lst.json_schema())