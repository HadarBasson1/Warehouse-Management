import random

def generate_id():
    return random.randint(1, 2**31 - 1)

async def generate_unique_id(collection):
    while True:
        new_id = generate_id()
        existing_item = collection.find_one({"id": new_id})
        if not existing_item:
            return new_id