from flask import Flask, jsonify, request
from flask_cors import CORS
import pymongo
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to the MongoDB instance
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["ProspectDb"]
collection = db["PlayFabUserData"]

# Load items data
with open('items.json', 'r', encoding='utf-8') as f:
    items_list = json.load(f)
    # Create a dictionary mapping key to item data
    items_data = {item['key']: item for item in items_list}

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    # Define the filter for the query
    filter = { "PlayFabId": "6D2AA73157A662EB", "Key": "Inventory" }

    # Execute the query and retrieve the results
    results = collection.find(filter)

    # Collect all inventory items
    all_items = []
    for result in results:
        # Parse the Value field as JSON
        inventory_data = json.loads(result["Value"])

        # Enhance each item with inGameName, description, rarity, and image path
        for item in inventory_data:
            base_item_id = item.get("baseItemId", "")
            item_info = items_data.get(base_item_id, {})

            item["inGameName"] = item_info.get("inGameName", base_item_id)
            item["description"] = item_info.get("description", "No description available")
            item["rarity"] = item_info.get("rarity", "Common")
            # Generate image path from baseItemId (lowercase, no spaces, avif format)
            image_name = item["inGameName"].lower().replace(" ", "")
            item["imagePath"] = f"images/{image_name}.avif"

        all_items.extend(inventory_data)

    # Sort items alphabetically by inGameName
    all_items.sort(key=lambda x: x.get("inGameName", "").lower())

    return jsonify(all_items)

@app.route('/api/inventory/update-amount', methods=['PUT'])
def update_item_amount():
    """
    Update the amount of an inventory item by itemId
    Expected JSON: { "itemId": "...", "amount": 10 }
    """
    try:
        data = request.get_json()
        item_id = data.get('itemId')
        new_amount = data.get('amount')

        if item_id is None or new_amount is None:
            return jsonify({'error': 'Missing itemId or amount'}), 400

        if not isinstance(new_amount, (int, float)) or new_amount < 0 or new_amount > 10:
            return jsonify({'error': 'Amount must be a non-negative number'}), 400

        # Find the inventory document
        filter_query = { "PlayFabId": "6D2AA73157A662EB", "Key": "Inventory" }
        inventory_doc = collection.find_one(filter_query)

        if not inventory_doc:
            return jsonify({'error': 'Inventory not found'}), 404

        # Parse inventory data
        inventory_data = json.loads(inventory_doc["Value"])

        # Find and update the item by itemId
        item_found = False
        for item in inventory_data:
            if item.get('itemId') == item_id:
                item['amount'] = new_amount
                item_found = True
                break

        if not item_found:
            return jsonify({'error': f'Item with itemId {item_id} not found'}), 404

        # Update MongoDB
        updated_value = json.dumps(inventory_data)
        result = collection.update_one(
            filter_query,
            {"$set": {"Value": updated_value}}
        )

        if result.modified_count > 0:
            return jsonify({
                'success': True,
                'itemId': item_id,
                'newAmount': new_amount
            }), 200
        else:
            return jsonify({'error': 'Failed to update'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
