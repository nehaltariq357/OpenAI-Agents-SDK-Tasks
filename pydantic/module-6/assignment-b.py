from pydantic import TypeAdapter
from rich import print

# Nested type: list of dict[str, int]
lst = TypeAdapter(list[dict[str, int]])

# Validate input
nested_type = lst.validate_python([{"math": "90"}, {"science": 85}])

print(nested_type)          # [{'math': 90}, {'science': 85}]
print(lst.json_schema())    # Schema print karega

# dump_json me validated object pass karo
print(lst.dump_json(nested_type))  
