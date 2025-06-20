import os
import json
from flask import Flask, request, jsonify, render_template
import redis
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 10001)),
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True,
    ssl=os.getenv("REDIS_USE_SSL", "false").lower() == "true"
)

def get_all_users():
    users = []
    for key in r.scan_iter("user:*"):
        user_id = key.split(":")[1]
        user_data = r.hgetall(key)
        if user_data:
            user_data["user_id"] = user_id
            users.append(user_data)
    return users

def get_all_products():
    products = []
    for key in r.scan_iter("product:*"):
        sku = key.split(":")[1]
        product_data = r.hgetall(key)
        if product_data:
            product_data["sku"] = sku
            products.append(product_data)
    return products

@app.route('/')
def index():
    users = get_all_users()
    products = get_all_products()
    return render_template('index.html', users=users, products=products)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user_id = data["user_id"]
    user_data = {
        "user_id": user_id,
        "name": data.get("name", ""),
        "email": data.get("email", "")
    }
    r.hset(f"user:{user_id}", mapping=user_data)
    return jsonify({"message": f"User {user_id} created."})

@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    sku = data["sku"]
    product_data = {
        "sku": sku,
        "name": data.get("name", ""),
        "description": data.get("description", ""),
        "qty": data.get("qty", "0"),
        "rating": data.get("rating", "0"),
        "price": data.get("price", "0.0")
    }
    r.hset(f"product:{sku}", mapping=product_data)
    return jsonify({"message": f"Product {sku} created."})

@app.route('/api/users')
def api_users():
    return jsonify(get_all_users())

@app.route('/api/products')
def api_products():
    return jsonify(get_all_products())

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    user_id = data["user_id"]
    sku = data["sku"]
    quantity = int(data.get("quantity", 1))
    r.hincrby(f"cart:{user_id}", sku, quantity)
    return jsonify({"message": f"Added {quantity} of {sku} to cart for user {user_id}."})

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    user_id = data["user_id"]
    sku = data["sku"]
    remove_qty = int(data.get("quantity", 1))

    cart_key = f"cart:{user_id}"
    current_qty = r.hget(cart_key, sku)

    if current_qty is None:
        return jsonify({"message": f"{sku} not found in cart for user {user_id}."}), 404

    new_qty = int(current_qty) - remove_qty

    if new_qty > 0:
        r.hset(cart_key, sku, new_qty)
        return jsonify({"message": f"Reduced {sku} by {remove_qty} for user {user_id}. New quantity: {new_qty}."})
    else:
        r.hdel(cart_key, sku)
        return jsonify({"message": f"Removed {sku} from cart for user {user_id}."})


@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    user_id = request.json["user_id"]
    r.delete(f"cart:{user_id}")
    return jsonify({"message": f"Cleared cart for user {user_id}."})

@app.route('/cart/summary/<user_id>', methods=['GET'])
def cart_summary(user_id):
    cart_key = f"cart:{user_id}"
    items = r.hgetall(cart_key)
    total = 0
    summary = []
    for sku, qty in items.items():
        product_data = r.hgetall(f"product:{sku}")
        price = float(product_data.get("price", 0))
        subtotal = price * int(qty)
        total += subtotal
        summary.append({
            "sku": sku,
            "name": product_data.get("name", ""),
            "quantity": qty,
            "price": price,
            "subtotal": subtotal
        })
    return jsonify({"user_id": user_id, "items": summary, "total": total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
