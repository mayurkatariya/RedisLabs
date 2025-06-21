# 🚀 RedisLabs

Welcome to **RedisLabs**! 
This repository documents key learnings and objectives for working with Redis, including setup, replication setup, data modeling, and application development.

---

## 📚 Problem Statement

Explore Redis by installing, configuring, and leveraging its features to build a scalable shopping cart application.

---

## 🎯 Objectives

1. **Install Redis Community Edition (CE) on a VM Instance**
  - Set up a Redis CE server for hands-on experimentation.

2. **Simulate & Load Data with Memtier**
  - Use [Memtier](https://github.com/RedisLabs/memtier_benchmark) to benchmark and populate your Redis instance.

3. **Deploy Redis Enterprise Edition**
  - Create a Redis Enterprise cluster 

4. **Database Replication**
  - Install a Redis database and configure it as a replica of your CE instance for redundancy and failover.

4. **Database Replication Script**
  - To prove replication is working, create a script to insert 100 digits and random numbers on CE and print them in Reverse Order from EE.
  - This script is created under VMrecplication Script Folder


6. **Build a Basic Shopping Cart Application**
  - **Data Modeling:**  
    - Design a simple, efficient data model for a shopping cart and user.
    - **Requirements:**
     - The cart can hold 0 to _n_ items.
     - Items are represented by SKUs.
     - The cart supports multiple quantities of each item.
     - Each cart is associated with a user.

--- This script is created under redis_shopping_cart_app_v0 folder. It has a seperate readme file with additional details

## 🛒 Example Data Model

```plaintext
User: {userid, name, email} 
Products:{sku, name, description, qty, rating, price}
Cart:UserId:{sku, qty}

```

---

## 💡 Tips
- Ensure data consistency between CE and Enterprise editions.
- Explore Redis modules for enhanced functionality.
- There is a separate readme file under both the folders on how to run the scripts and the application

