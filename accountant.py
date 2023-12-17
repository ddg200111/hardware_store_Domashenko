from flask import Flask, jsonify, request
from flasgger import Swagger
from datetime import datetime
from orders import orders
import json

app = Flask(__name__)
swagger = Swagger(app)

# Endpoint to show all orders
@app.route('/accountant/orders', methods=['GET'])
def get_cashier_orders():
    """
    Get all orders.

    ---
    responses:
      200:
        description: A list of orders.
        content:
          application/json:
            schema:
              type: object
              properties:
                orders:
                  type: array
                  items:
                    type: object
                      # Structure of an individual order
                      # id: Order ID
                      # name: Name of the buyer
                      # productId: ID of the product being ordered
                      # price: Price of the ordered product
                      # date: Date of the order
                      # status: Status of the order (Accepted, Done, Paid)
    """
    return json.dumps({'orders': orders}, indent=2)

# Endpoint to get orders within a date range
@app.route('/accountant/orders_by_date', methods=['GET'])
def get_orders_by_date():
    """
    Get a list of orders within a specified date range.

    ---
    parameters:
      - name: start_date
        in: query
        type: string
        format: date
        required: true
        description: The start date of the range (YYYY-MM-DD).
      - name: end_date
        in: query
        type: string
        format: date
        required: true
        description: The end date of the range (YYYY-MM-DD).
    responses:
      200:
        description: A list of orders within the specified date range.
        schema:
          type: object
          properties:
            orders:
              type: array
              items:
                type: object
                  # Structure of an individual order
                  # id: Order ID
                  # name: Name of the customer
                  # productId: ID of the ordered product
                  # price: Price of the ordered product
                  # date: Date of the order
                  # status: Status of the order
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
      400:
        description: Bad request. Invalid date format or missing parameters.
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        # Parse dates from string to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        # Filter orders within the specified date range
        filtered_orders = [
            order for order in orders
            if start_date <= datetime.strptime(order['date'], '%Y-%m-%d') <= end_date
        ]

        return jsonify({'orders': filtered_orders})

    except ValueError as e:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
