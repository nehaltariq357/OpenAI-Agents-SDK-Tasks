
import asyncio
from agents import SQLiteSession

async def main():
    session =SQLiteSession(session_id="memory_operations",db_path="test.db")

    # Add some conversation items manually
    conversation_item = [
        {"role":"user","content":"Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help you?"},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I don't have access to weather data."}
    ]

    await session.add_items(conversation_item)
    print("Added conversation to memory!")

    # View all items in memory
    items = await session.get_items()
    print(f"\nMemory contains {len(items)} items:")
    for item in items:
        print(f"{item["role"]}: {item["content"]}")

    # Clear all memory
    await session.clear_session()
    print("\nCleared all memory!")

    # Verify memory is empty
    items = await session.get_items()
    print(f"\nMemory contains {len(items)} items:")











# Run the async demo
asyncio.run(main())