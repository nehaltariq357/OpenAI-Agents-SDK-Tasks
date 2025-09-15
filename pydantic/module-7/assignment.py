from pydantic import BaseModel

class Item(BaseModel):
    name:str
    price:float

class Order(BaseModel):
    id:int
    items:list[Item]

o = Order.model_validate({
    "id":1,
    "items":[{
        "name":"bool",
        "price":10.33
    },
    {"name": "Pen", "price": 5}
    ]
})

print(o.model_dump())