#REDIS LAB 
# This script demonstrates how to insert data into a Redis OSS instance and retrieve it from a Redis Enterprise instance.
# It connects to both instances, performs data insertion, and retrieves the data to verify replication.
import redis
import random

REDIS_HOST_CE = '35.231.111.176'  # IP for Redis OSS (Community Edition) instance
REDIS_PORT_CE = 10001 #Port for Redis CE instance

REDIS_HOST_EE = '35.237.25.44'  # IP for Redis Enterprise Edition instance
REDIS_PORT_EE = 12000 #Port for Redis EE instance

#Test connection to Redis CE and EE instances   
try:
    r_ce = redis.Redis(host=REDIS_HOST_CE, port=REDIS_PORT_CE, decode_responses=True)
    r_ce.ping()
    print(f"🟢CE: Connection Success: Client ID is {r_ce.client_id()}")
    print(f"🟢 Successfully connected to Redis CE at {REDIS_HOST_CE}:{REDIS_PORT_CE}")
except redis.ConnectionError as e:
    print(f"❌ Failed to connect to Redis CE at {REDIS_HOST_CE}:{REDIS_PORT_CE}")
    print("Error:", str(e))
    exit(1)

try:
    r_ee = redis.Redis(host=REDIS_HOST_EE, port=REDIS_PORT_EE, decode_responses=True)
    r_ee.ping()
    print(f"🟢EE: Connection Success: Client ID is {r_ee.client_id()}")
    print(f"🟢 Successfully connected to Redis EE at {REDIS_HOST_EE}:{REDIS_PORT_EE}")
except redis.ConnectionError as e:
    print(f"❌ Failed to connect to Redis EE at {REDIS_HOST_EE}:{REDIS_PORT_EE}")
    print("Error:", str(e))
    exit(1)

# Defining keys for Redis Lists
num_list = 'lab:num_list'
rand_list = 'lab:rand_list'

# Reset keys - To delete existing keys if they exist due to previous runs
r_ce.delete(num_list)
r_ce.delete(rand_list)
print(f"🗑️ Cleared existing keys: {num_list}, {rand_list}")

# Insert values 1 to 100 
print(f"Inserting new keys 1-100") # Insert values 1 to 100
for i in range(1, 101):
    r_ce.lpush(num_list, i) # To push integers from left side of the list
    print(i,end=' ', flush=True)  #end & flush=True to print on the same line

print(f"✅ Inserted integers 1–100 into CE_REDIS key: {num_list}")

# Insert 100 random values
print(f"Inserting random keys between 1-1000")
for _ in range(100):
    rand_val=random.randint(1, 1000) #generate random value between 1 and 1000
    r_ce.lpush(rand_list,rand_val) # To push any random values between 1 to 1000 from left side of the list
    print(rand_val,end=' ', flush=True)
print()
print(f"✅ Inserted 100 random values into key: CE_REDIS key {rand_list}")

# Retrieve values from Redis EE
#int_values_reversed = [r_ee.lpop(num_list) for _ in range(100)] # LPOP because we need reverse order of the list i.e Stack Functionality LIFO
#rand_values_reversed = [r_ee.lpop(rand_list) for _ in range(100)]

# Retrieve values from Redis EE without destroying the list
int_values_reversed = r_ee.lrange(num_list, 0, 99)  # Get first 100 elements (leftmost, i.e., most recently pushed)
rand_values_reversed = r_ee.lrange(rand_list, 0, 99)

print("🔁🔁 Revered Integers: PRINTING FROM EE", [int(x) for x in int_values_reversed]) 
print("🔁🔁 Reversed Randoms: PRINTING FROM EE", [int(x) for x in rand_values_reversed])

print("🎉🎉 Redis insert from CE and read-back from EE operations completed successfully.This also proves replication is working")
