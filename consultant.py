from flask import Flask, jsonify, request
from flasgger import Swagger
from orders import orders
import json

app = Flask(__name__)
swagger = Swagger(app)

# Function to write orders to orders.json
def write_orders_to_json():
    with open('orders.json', 'w') as file:
        json.dump(orders, file, indent=2)

# Endpoint to show all accepted orders
@app.route('/consultant/accepted_orders', methods=['GET'])
def get_accepted_orders():
    """
    Get a list of all accepted orders.

    ---
    responses:
      200:
        description: A list of accepted orders.
        schema:
          type: object
          properties:
            accepted_orders:
              type: array
              items:
                type: object
                  # Structure of an individual accepted order
                  # id: Order ID
                  # name: Name of the customer
                  # productId: ID of the ordered product
                  # price: Price of the ordered product
                  # date: Date of the order
                  # status: Status of the order (Accepted)
                  # Description of each property added for clarity
                properties:
                  id:
                    type: integer
                    description: The order ID.
                  name:
                    type: string
                    description: The customer's name.
                  productId:
                    type: integer
                    description: The product ID.
                  price:
                    type: number
                    description: The order price.
                  date:
                    type: string
                    format: date
                    description: The order date.
                  status:
                    type: string
                    description: The order status.
    """
    accepted_orders = [order for order in orders if order['status'] == 'Accepted']
    return jsonify({'accepted_orders': accepted_orders})

# Endpoint to update the status of an existing order
@app.route('/consultant/update_status/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """
    Update the status of an existing order.

    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
        description: The ID of the order to update.
      - name: status
        in: body
        type: string
        required: true
        description: The new status for the order.

    responses:
      200:
        description: Order status updated successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              description: A success message.
            order:
              type: object
                # Structure of the updated order
                # id: Order ID
                # name: Name of the customer
                # productId: ID of the ordered product
                # price: Price of the ordered product
                # date: Date of the order
                # status: The new status of the order
              description: The updated order details.
              properties:
                id:
                  type: integer
                  description: The updated order ID.
                name:
                  type: string
                  description: The updated customer's name.
                productId:
                  type: integer
                  description: The updated product ID.
                price:
                  type: number
                  description: The updated order price.
                date:
                  type: string
                  format: date
                  description: The updated order date.
                status:
                  type: string
                  description: The updated order status.
      404:
        description: Order not found error.
        schema:
          type: object
          properties:
            error:
              type: string
              description: The error message.
    """
    new_status = "Done"
    
    for order in orders:
        if order['id'] == order_id:
            order['status'] = new_status
            write_orders_to_json()  # Write the updated orders to orders.json
            return jsonify({'message': f'Status of order {order_id} updated to {new_status}', 'order': order})

    return jsonify({'error': f'Order with ID {order_id} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5002)
