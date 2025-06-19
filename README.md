# 🚀 RedisLabs

Welcome to **RedisLabs**! This repository documents key learnings and objectives for working with Redis, including setup, data modeling, and application development.

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
  - Create a Redis Enterprise cluster for advanced features and high availability.

4. **Database Replication**
  - Install a Redis database and configure it as a replica of your CE instance for redundancy and failover.

4. **Database Replication Script**
  - To prove replication is working, Create a script to insert 100 digits and random numbers on CE and print them in Reverse Order from CE 


6. **Build a Basic Shopping Cart Application**
  - **Data Modeling:**  
    - Design a simple, efficient data model for a shopping cart and user.
    - **Requirements:**
     - The cart can hold 0 to _n_ items.
     - Items are represented by SKUs.
     - The cart supports multiple quantities of each item.
     - Each cart is associated with a user.

---

## 🛒 Example Data Model

```plaintext
User: user:123
  └── Cart: cart:123
      ├── item:sku_001 → 2
      ├── item:sku_002 → 1
      └── item:sku_005 → 4
```

---

## 💡 Tips

- Use Redis hashes or sorted sets for efficient cart management.
- Ensure data consistency between CE and Enterprise editions.
- Explore Redis modules for enhanced functionality.

