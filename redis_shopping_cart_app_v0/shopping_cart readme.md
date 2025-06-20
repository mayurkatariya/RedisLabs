
# 🛒 Redis Shopping Cart App

A full-stack shopping cart application built with **Flask**, **Redis**, **Bootstrap**, and **JavaScript**. This app allows users to register, add products, manage a shopping cart, and get live cart summaries — all using Redis for high-speed backend operations.

---

## 🚀 Features

- ✅ Create and view users  
- ✅ Create and view products  
- ✅ Add/remove/clear products in cart  
- ✅ Dynamic cart summary calculation  
- ✅ Redis-backed storage using hashes  
- ✅ Live dropdown updates & summary refresh  
- ✅ Clean Bootstrap-based UI

---

## 📁 Project Structure

```

RedisLabs/redis_shopping_cart_app_v0/
│
├── app/
│   ├── app.py               # Flask backend
│   ├── templates/
│   │   └── index.html       # Frontend HTML + JS
│   └── .env                 # Redis connection config
│
├── requirements.txt         # Python dependencies
└── shopping_cart README.md  # Shopping Cart Project guide  
```

---

## 🛠️ Setup Instructions

### 00 Install Python & PIP Packages 
```bash
sudo apt update
sudo apt install python3
sudo apt install python-pip3
``` 

### 1. Clone the Repository

```bash
git clone https://github.com/mayurkatarya/redis-cart-app.git
cd RedisLabs/redis_shopping_cart_app_v0/
```

### 2. Create and Activate a Virtual Environment

```bash
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
```

### 3. Install Required Packages

```bash
pip3 install -r requirements.txt
```

### 4. Configure Redis Connection

Create a `.env` file inside the `app/` directory:

```ini
REDIS_HOST=localhost
REDIS_PORT=12000
REDIS_PASSWORD=
REDIS_USE_SSL=false
```

Adjust settings as needed for your Redis server.

---

## ▶️ Run the Application

```bash
cd app
python app.py
```

By default, the app runs on: [http://localhost:5001](http://localhost:5001)

---

## 🌍 Accessing the App from Your Browser (Remote VM)

To access a remote Redis Flask app locally using an SSH tunnel:

### Step 1: Create Tunnel

```bash
ssh -L 5001:localhost:5001 -i path/to/your-key.pem ubuntu@<remote-vm-ip>
```

- Replace `path/to/your-key.pem` with your SSH private key  
- Replace `<remote-vm-ip>` with your VM's public IP

### Step 2: Open in Browser

```
http://localhost:5001
```

✅ Now you can use the app in your browser as if it were running locally.

---

## 📋 Requirements

- Python 3.7+
- Redis server (Community or Enterprise)
- pip packages:
  - `flask`
  - `redis`
  - `python-dotenv`

To install manually:

```bash
pip install flask redis python-dotenv
```

---

## 🧠 Redis Data Structure Notes

- `user:{user_id}` → Hash (name, email)  
- `product:{sku}` → Hash (name, description, qty, rating, price)  
- `cart:{user_id}` → Hash (sku → quantity)

---

## 📄 License

MIT © Your Name
