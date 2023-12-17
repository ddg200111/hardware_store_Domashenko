import json
import os

# Check if 'orders.json' file exists, and create it if not
orders_file_path = 'orders.json'

if not os.path.exists(orders_file_path):
    # If the file doesn't exist, create it and initialize it with an empty list
    with open(orders_file_path, 'w') as file:
        json.dump([], file)

# Read data from orders.json
with open(orders_file_path, 'r') as file:
    # Load existing data from the file into the 'orders' variable
    orders = json.load(file)
