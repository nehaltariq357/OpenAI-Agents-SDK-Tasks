import os
from agents import Agent,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,Runner
from dotenv import load_dotenv
from rich import print
from pydantic import BaseModel
from typing import Optional,List

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
# Tracing disabled
set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.5-flash",
)

# Define your data structure
class ProductInfo(BaseModel):
    name: str                           # Text
    price: float                        # Decimal number
    in_stock: bool                      # True/False
    categories: List[str]               # List of text items
    discount_percent: Optional[int] = 0 # Optional number, default 0
    reviews_count: int                  # Whole number




agent = Agent(
    name="ProductExtractor",
    instructions="Extract product information from product descriptions.",
    model=model,
    output_type=ProductInfo   # This is the magic!
)

def main():
    # Test it
    result = Runner.run_sync(
        starting_agent=agent,
        input="The iPhone 15 Pro costs $999.99, it's available in electronics and smartphones categories, currently in stock with 1,247 reviews.",
    )


    # Now you get perfect structured data!
    print("Type:", type(result.final_output))      
    print("Product:", result.final_output.name)         # "iPhone 15 Pro"
    print("Price:", result.final_output.price)          # 999.99
    print("In Stock:", result.final_output.in_stock)    # True
    print("Categories:", result.final_output.categories) # ["electronics", "smartphones"]
    print("Reviews:", result.final_output.reviews_count) # 1247



if __name__ == "__main__":
    main()






