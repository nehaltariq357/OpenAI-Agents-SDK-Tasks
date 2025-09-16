from pydantic import TypeAdapter,Field
from typing_extensions import Annotated
from typing import TypedDict

class Book(TypedDict):
    title:Annotated[str,Field(...,min_length=3)]
    pages:Annotated[int,Field(...,ge=1)]

ta = TypeAdapter(Book)

book=ta.validate_python({
    "title":"python",
    "pages":250
})

print(book)

print(ta.dump_json(book))