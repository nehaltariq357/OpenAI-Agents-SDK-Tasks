from pydantic import BaseModel,Field,ValidationError
from typing_extensions import Annotated
from rich import print
class Product(BaseModel):
    # Name kam se kam 2 characters ka hona chahiye
    name:str = Field(...,min_length=2,description="Product name")

    # Price zero ya usse zyada hona chahiye
    pirce:float = Field(...,ge=0,description="Product price (>=0)")

    # Tags ek list hai jisme har item kam se kam 2 letters ka ho
    tags:list[Annotated [str, Field(min_length=2)]]  = []

try:
    p1 = Product(name="laptop",pirce=1200,tags=["IT","PC"])
    print(p1.model_dump()) # {'name': 'laptop', 'pirce': 1200.0, 'tags': ['IT', 'PC']}
    #Agar tum print(Product.model_json_schema()) karoge to tumhe constraints clearly dikhai denge:
    print(p1.model_json_schema())
except ValidationError as e:
    print("validation error: ",e)