import pymongo
import json

# Connect to the MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["ProspectDb"]

# Get the PlayFabUserData collection
collection = db["PlayFabUserData"]

# Define the filter for the query #was 19B1910D144C7E5E
filter = { "PlayFabId": "6D2AA73157A662EB", "Key": "Inventory" }

# Execute the query and retrieve the results
results = collection.find(filter)

# Collect all inventory items
all_items = []
for result in results:
    # Parse the Value field as JSON
    inventory_data = json.loads(result["Value"])
    all_items.extend(inventory_data)

# Sort items alphabetically by baseItemId
all_items.sort(key=lambda x: x.get("baseItemId", ""))

# Print table header
print(f"{'BaseItemId':<30} | {'RolledPerks':<50} | {'Amount':>10}")
print("-" * 95)

# Print each row in table format
for item in all_items:
    base_item_id = item.get("baseItemId", "N/A")
    rolled_perks = str(item.get("rolledPerks", []))
    amount = item.get("amount", 0)

    print(f"{base_item_id:<30} | {rolled_perks:<50} | {amount:>10}")