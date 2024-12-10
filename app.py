from datetime import datetime
import math
import uuid
from flask import Flask, abort, request, jsonify
from openapi_core import OpenAPI
from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator

from point_rules import calculate_points

app = Flask(__name__)

# Load the OpenAPI specification
openapi = OpenAPI.from_file_path('api.yml')
openapi_validated = FlaskOpenAPIViewDecorator(openapi)

# simple in-memory storage
RECEIPT_STORAGE = {}

def receipt_processor(receipt_data):
    """
    Processes the receipt data and generate the id for storage.
    
    Keyword arguments: receipt_data
    Return: returns generated key for the point storage
    """
    # retailer = receipt_data['retailer']
    # purchase_date = receipt_data['purchaseDate']
    # purchase_time_str = receipt_data['purchaseTime']
    # items = receipt_data['items']
    # total_value = float(receipt_data['total'])
    receipt_data['total'] = float(receipt_data['total'])
    
    storage_id = str(uuid.uuid4())
    
    RECEIPT_STORAGE[storage_id] = receipt_data
    
    return storage_id


@app.route('/receipts/process', methods=['POST'])
@openapi_validated
def process_receipts():
    # Process the validated request data
    data = request.openapi.body
    generated_id = receipt_processor(data)
    
    return jsonify({"id": generated_id}), 200



@app.route('/receipts/<id>/points', methods=['GET'])
@openapi_validated
def get_points(id):
    valid_id = request.openapi.parameters.path['id']
    print(valid_id, type(valid_id))
    if valid_id not in RECEIPT_STORAGE:
        abort(404, description="No receipt found for that id")
    
    points = calculate_points(RECEIPT_STORAGE[valid_id])
        
    return jsonify({"points": points})

if __name__ == "__main__":
    app.run(port=8080, debug=True)