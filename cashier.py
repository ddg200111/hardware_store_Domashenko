from flask import Flask, json, request, jsonify, Response
from flasgger import Swagger
import json
import os
from datetime import datetime, timedelta
from orders import orders
from products import products

app = Flask(__name__)
swagger = Swagger(app)

# Function to write orders to orders.json
def write_orders_to_json():
    with open('orders.json', 'w') as file:
        json.dump(orders, file, indent=2)

# Function to get the price and date based on productId
def get_product_info_by_id(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return {'price': product['price'], 'date': product['date']} if product else None

# Function to check if the difference between two dates is more than one month
def is_more_than_one_month(date1, date2):
    date1 = datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.strptime(date2, '%Y-%m-%d')
    difference = date1 - date2
    return difference > timedelta(days=30)

# Endpoint to add a new order
@app.route('/cashier/add_new_order', methods=['POST'])
def add_new_order():
    """
    Add a new order.

    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: The name of the buyer.
            productId:
              type: integer
              description: The ID of the product being ordered.
    responses:
      201:
        description: Order added successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                order:
                  type: object
                      # Structure of the added order
                      # id: Order ID
                      # name: Name of the buyer
                      # productId: ID of the product being ordered
                      # price: Price of the ordered product
                      # date: Date of the order
                      # status: Status of the order (Accepted, Done, Paid)
      400:
        description: Bad request. Missing or invalid parameters.
    """
    new_order = request.get_json()

    # Set the 'date' field to the current date in the format (year, month, day)
    current_date = datetime.now().strftime('%Y-%m-%d')
    new_order['date'] = current_date

    # Set the 'status' field to "Accepted"
    new_order['status'] = "Accepted"

    if not orders:
        new_order['id'] = 1  # If the list is empty, set the id to 1
    else:
        # Assuming the new order has a unique 'id'
        new_order_id = max(order['id'] for order in orders) + 1
        new_order['id'] = new_order_id

    # Get product information based on 'productId'
    product_id = new_order.get('productId')
    if product_id is not None:
        product_info = get_product_info_by_id(product_id)

        if product_info:
            # Check the difference between dates and adjust the price if more than one month
            if is_more_than_one_month(current_date, product_info['date']):
                new_order['price'] = round(0.8 * product_info['price'], 2)
            else:
                new_order['price'] = round(product_info['price'], 2)

    # Explicitly define the order of fields
    ordered_fields = ['id', 'name', 'productId', 'price', 'date', 'status']
    new_order = {key: new_order[key] for key in ordered_fields if key in new_order}

    orders.append(new_order)

    # Write the updated orders to orders.json
    write_orders_to_json()

    return jsonify({'message': 'Order added successfully', 'order': new_order}), 201

# Endpoint to show all orders with status "Done"
@app.route('/cashier/done_orders', methods=['GET'])
def get_done_items():
    """
    Get all items with status "Done".

    ---
    responses:
      200:
        description: A list of items with status "Done".
        content:
          application/json:
            schema:
              type: object
              properties:
                done_items:
                  type: array
                  items:
                    type: object
                      # Structure of an individual item with status "Done"
                      # id: Order ID
                      # name: Name of the buyer
                      # productId: ID of the product being ordered
                      # price: Price of the ordered product
                      # date: Date of the order
                      # status: Status of the order (Done)
    """
    done_items = [item for item in orders if item['status'] == 'Done']
    return jsonify({'done_items': done_items})

# Endpoint to change the status of an existing order with status "Done" to "Paid"
@app.route('/cashier/mark_paid/<int:item_id>', methods=['PUT'])
def mark_item_paid(item_id):
    """
    Change the status of an item with status "Done" to "Paid".

    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: The ID of the item to mark as "Paid".
    responses:
      200:
        description: Status of the item updated successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                item:
                  type: object
                      # Structure of the updated item
                      # id: Order ID
                      # name: Name of the buyer
                      # productId: ID of the product being ordered
                      # price: Price of the ordered product
                      # date: Date of the order
                      # status: Status of the order (Paid)
      404:
        description: Item with the specified ID not found or not in "Done" status.
    """
    new_status = "Paid"
    
    for item in orders:
        if item['id'] == item_id and item['status'] == 'Done':
            item['status'] = new_status
            write_orders_to_json()  # Write the updated orders to orders.json
            return jsonify({'message': f'Status of item {item_id} updated to {new_status}', 'item': item})

    return jsonify({'error': f'Item with ID {item_id} not found or not in "Done" status'}), 404

# Endpoint to show all orders with status "Paid"
@app.route('/cashier/paid_orders', methods=['GET'])
def get_paid_items():
    """
    Get all items with status "Paid".

    ---
    responses:
      200:
        description: A list of items with status "Paid".
        content:
          application/json:
            schema:
              type: object
              properties:
                paid_items:
                  type: array
                  items:
                    type: object
                      # Structure of an individual item with status "Paid"
                      # id: Order ID
                      # name: Name of the buyer
                      # productId: ID of the product being ordered
                      # price: Price of the ordered product
                      # date: Date of the order
                      # status: Status of the order (Paid)
    """
    paid_items = [item for item in orders if item['status'] == 'Paid']
    return jsonify({'paid_items': paid_items})

# Function to get product information by ID
def get_product_info_by_id(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return product if product else None

# Function to generate a bill based on order ID
def generate_bill(order_id):
    order = next((o for o in orders if o['id'] == order_id and o['status'] == 'Paid'), None)
    if order:
        current_date = datetime.now().strftime('%Y-%m-%d')
        formatted_date = datetime.now().strftime('%d %B, %Y')  # Format date as day, month in words, year

        # Create a separate JSON table with Product name, Price, Discount, and Sum
        json_table = []
        product_id = order.get('productId')
        product_info = get_product_info_by_id(product_id)
        if product_id is not None and product_info is not None:
            # Check if the order price is less than the product price
            if order['price'] < product_info['price']:
                discount = '20% off'
            else:
                discount = ''

            # Calculate the sum (order price)
            order_sum = order['price']

            json_table.append({
                "№": 1,
                "Product name": product_info['name'],
                "Price": product_info['price'],
                "Discount": discount,
                "Sum": order_sum
            })

        return {
            "bill_id": order['id'],
            "date": formatted_date,
            "provider": "Store details",
            "buyer": order.get('name', 'N/A'),
            "json_table": json_table
        }
    else:
        return None

# Endpoint to generate a bill based on order ID
@app.route('/cashier/generate_bill/<int:order_id>', methods=['GET'])
def generate_bill_endpoint(order_id):
    """
    Generate a bill based on order ID.

    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The ID of the order to generate a bill for.
    responses:
      200:
        description: Bill generated successfully.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                bill:
                  type: object
                      # Structure of the generated bill
                      # bill_id: Order ID
                      # date: Formatted date of the bill
                      # provider: Provider details
                      # buyer: Name of the buyer
                      # json_table: Table containing product details in JSON format
                      #    - Structure of the JSON table
                      #      "№": Serial number
                      #      "Product name": Name of the product
                      #      "Price": Price of the product
                      #      "Discount": Discount applied (if any)
                      #      "Sum": Total sum of the product
    404:
      description: Order with the specified ID not found or not in "Paid" status.
    """
    bill_info = generate_bill(order_id)
    if bill_info:
        json_response = json.dumps({'message': 'Bill generated successfully', 'bill': bill_info}, indent=2, sort_keys=False)
        return Response(response=json_response, status=200, mimetype='application/json')
    else:
        return jsonify({'error': f'Order with ID {order_id} not found or not in "Paid" status'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
