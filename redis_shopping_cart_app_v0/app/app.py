import os
import json
from flask import Flask, request, jsonify, render_template
import redis
from dotenv import load_dotenv

# Load environment variables from a .env file (useful for credentials and configs)
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Connect to the Redis database using environment variables
# If environment variables are missing, use default values
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),  # Redis host (default: localhost)
    port=int(os.getenv("REDIS_PORT", 10001)),   # Redis port (default: 10001)
    password=os.getenv("REDIS_PASSWORD", ""),   # Redis password (default: none)
    decode_responses=True,                      # Always decode responses to strings
    ssl=os.getenv("REDIS_USE_SSL", "false").lower() == "true"  # Use SSL if specified
)

# -------------------------------------------------
# Helper function to retrieve all users from Redis
# -------------------------------------------------
def get_all_users():
    users = []  # Initialize an empty list to store user data dictionaries

    # Iterate over all keys in Redis that match the pattern 'user:*'
    # The pattern 'user:*' ensures only user-related hashes are scanned.
    for key in r.scan_iter("user:*"):
        # Extract the user_id from the key.
        # Example: if key is 'user:123', user_id will be '123'.
        user_id = key.split(":")[1]

        # Retrieve all fields and their values for this user from the Redis hash.
        # r.hgetall returns a dictionary representing the user's data.
        user_data = r.hgetall(key)

        # Check if we successfully retrieved user data.
        # This prevents adding empty or non-existent user hashes to the list.
        if user_data:
            # Add the user_id into the user_data dictionary for easier reference downstream,
            # since the user_id is derived from the key and not guaranteed to be in the hash itself.
            user_data["user_id"] = user_id

            # Append the complete user data dictionary (with user_id) to the users list.
            users.append(user_data)

    # After iterating through all matching Redis keys, return the complete list of user data dictionaries.
    return users

# -------------------------------------------------
# Helper function to retrieve all products from Redis
# -------------------------------------------------
def get_all_products():
    products = []  # Initialize an empty list to store product data dictionaries

    # Iterate over all keys in Redis that match the pattern 'product:*'
    # This pattern ensures we only process product hashes.
    for key in r.scan_iter("product:*"):
        # Extract the SKU (product code) from the key, e.g. 'product:sku123' → 'sku123'
        sku = key.split(":")[1]

        # Retrieve all fields and values for this product from the Redis hash
        product_data = r.hgetall(key)

        # Only add non-empty products (ignore keys with no data)
        if product_data:
            # Add the sku to the product data for reference
            product_data["sku"] = sku
            products.append(product_data)

    # Return the complete list of product data
    return products

# -------------------------------------------------
# Home page route: display users and products
# -------------------------------------------------
@app.route('/')
def index():
    # Fetch all users and products from Redis to show on the homepage
    users = get_all_users()
    products = get_all_products()
    # Render the template with the users and products data
    return render_template('index.html', users=users, products=products)

# -------------------------------------------------
# API endpoint to create a new user
# -------------------------------------------------
@app.route('/user', methods=['POST'])
def create_user():
    # Get the JSON data sent in the request body
    data = request.json
    user_id = data["user_id"]  # Expect a user_id to be provided

    # Build the user data dictionary (provide defaults for missing fields)
    user_data = {
        "user_id": user_id,
        "name": data.get("name", ""),
        "email": data.get("email", "")
    }
    # Store the user data as a Redis hash under the key 'user:<user_id>'
    r.hset(f"user:{user_id}", mapping=user_data)
    return jsonify({"message": f"User {user_id} created."})

# -------------------------------------------------
# API endpoint to create a new product
# -------------------------------------------------
@app.route('/product', methods=['POST'])
def create_product():
    # Get the JSON data sent in the request body
    data = request.json
    sku = data["sku"]  # Expect a SKU to be provided

    # Build the product data dictionary (provide defaults for missing fields)
    product_data = {
        "sku": sku,
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "qty": data.get("qty", "0"),
        "rating": data.get("rating", "0"),
        "price": data.get("price", "0.0")
    }
    # Store the product data as a Redis hash under the key 'product:<sku>'
    r.hset(f"product:{sku}", mapping=product_data)
    return jsonify({"message": f"Product {sku} created."})

# -------------------------------------------------
# API endpoint to get all users as JSON
# -------------------------------------------------
@app.route('/api/users')
def api_users():
    return jsonify(get_all_users())

# -------------------------------------------------
# API endpoint to get all products as JSON
# -------------------------------------------------
@app.route('/api/products')
def api_products():
    return jsonify(get_all_products())

# -------------------------------------------------
# API endpoint to add a product to a user's cart
# -------------------------------------------------
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data["user_id"]
    sku = data["sku"]
    quantity = int(data.get("quantity", 1))  # Default to 1 if not given

    # Increment the quantity of the product in the user's cart
    # The cart is stored as a hash: key 'cart:<user_id>', field '<sku>'
    r.hincrby(f"cart:{user_id}", sku, quantity)
    return jsonify({"message": f"Added {quantity} of {sku} to cart for user {user_id}."})

# -------------------------------------------------
# API endpoint to remove a product (or reduce its quantity) from a user's cart
# -------------------------------------------------
@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    user_id = data["user_id"]
    sku = data["sku"]
    remove_qty = int(data.get("quantity", 1))  # Default to removing 1 if not specified

    cart_key = f"cart:{user_id}"  # Format the cart key for this user
    current_qty = r.hget(cart_key, sku)  # Fetch current quantity of this product in the cart

    if current_qty is None:
        # The product is not in the cart; return 404 error
        return jsonify({"message": f"{sku} not found in cart for user {user_id}."}), 404

    new_qty = int(current_qty) - remove_qty  # Calculate the new quantity after removal

    if new_qty > 0:
        # If the new quantity is still positive, update the cart with the reduced quantity
        r.hset(cart_key, sku, new_qty)
        return jsonify({"message": f"Reduced {sku} by {remove_qty} for user {user_id}. New quantity: {new_qty}."})
    else:
        # If the new quantity is zero or less, remove the product from the cart
        r.hdel(cart_key, sku)
        return jsonify({"message": f"Removed {sku} from cart for user {user_id}."})

# -------------------------------------------------
# API endpoint to clear all items from a user's cart
# -------------------------------------------------
@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    user_id = request.json["user_id"]
    # Delete the entire cart hash for this user
    r.delete(f"cart:{user_id}")
    return jsonify({"message": f"Cleared cart for user {user_id}."})

# -------------------------------------------------
# API endpoint to provide a summary of a user's cart
# Includes total price and detailed info for each item
# -------------------------------------------------
@app.route('/cart/summary/<user_id>', methods=['GET'])
def cart_summary(user_id):
    cart_key = f"cart:{user_id}"   # Format the cart key for this user
    items = r.hgetall(cart_key)    # Get all items (SKU: quantity) from the cart

    total = 0                      # Initialize total cart value
    summary = []                   # List to hold detailed item summaries

    # Loop through each product in the cart
    for sku, qty in items.items():
        product_data = r.hgetall(f"product:{sku}")  # Fetch product details from Redis
        price = float(product_data.get("price", 0)) # Get product price (default to 0 if missing)
        subtotal = price * int(qty)                 # Calculate subtotal for this item
        total += subtotal                          # Add to the running total

        # Build a summary dictionary for this item
        summary.append({
            "sku": sku,
            "name": product_data.get("name", ""),
            "quantity": qty,
            "price": price,
            "subtotal": subtotal
        })

    # Return a JSON summary of the cart, including user_id, items, and total cart value
    return jsonify({"user_id": user_id, "items": summary, "total": total})

# -------------------------------------------------
# Start the Flask development server if this script is run directly
# -------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
```

Let me know if you want even more granular comments for any specific function or additional explanations for edge cases or best practices!
