from flask import Flask, request, jsonify
from openapi_core import OpenAPI
from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator

app = Flask(__name__)

# Load the OpenAPI specification
openapi = OpenAPI.from_file_path('api.yml')
openapi_validated = FlaskOpenAPIViewDecorator(openapi)

@app.route('/receipts/process', methods=['POST'])
@openapi_validated
def process_receipts():

    # Process the validated request data
    data = request.openapi.body
    print("validated ->", data)
    
    return jsonify({"id": "some-generated-id"}), 200

@app.route('/receipts/<id>/points', methods=['GET'])
@openapi_validated
def get_points(id):
    print(request.openapi.parameters.path['id'])
    return jsonify({"points": 100})

if __name__ == "__main__":
    app.run(port=8080, debug=True)