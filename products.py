from flask import Flask, jsonify, Response
from flasgger import Swagger
import json

app = Flask(__name__)
Swagger(app)

# Sample data (fixtures)
products = [
    {"id": 1, "name": "Microwave Gorenje MO17E1W", "price": 2720.00, "date": "2023-10-03"},
    {"id": 2, "name": "Robot vacuum Xiaomi Mi Robot Vacuum S10+ White", "price": 14600.00, "date": "2023-12-02"},
    {"id": 3, "name": "Electric shaver Philips razor 7000 series S7882/55", "price": 7200.00, "date": "2023-12-04"},
    {"id": 4, "name": "Coffee machine Krups EA895N10", "price": 18425.00, "date": "2023-10-03"},
    {"id": 5, "name": "Electric fireplace Artiflame AF23S", "price": 15790.00, "date": "2023-12-02"}
]

# Endpoint to show all items
@app.route('/products', methods=['GET'])
def get_all_products():
    """
    Get a list of all products.

    ---
    responses:
      200:
        description: A list of products.
        schema:
          type: object
          properties:
            products:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The product ID.
                  name:
                    type: string
                    description: The product name.
                  price:
                    type: number
                    description: The product price.
                  date:
                    type: string
                    format: date
                    description: The date the product was added.
    """
    # Extract necessary fields from each product and create a new list
    ordered_products = [{key: product[key] for key in ["id", "name", "price", "date"]} for product in products]
    
    # Convert the list to a JSON response
    json_response = json.dumps({"products": ordered_products})
    
    # Return the JSON response as a Flask Response object
    return Response(json_response, content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
