import os
from flask import Flask, jsonify, request

app = Flask(__name__)

#New code for challenege one
# Shared inventory dataset
ITEMS = [
    {'id': 1, 'name': 'router', 'stock': 8},
    {'id': 2, 'name': 'switch', 'stock': 3}
]
#End
@app.get('/')
def index():
    return jsonify(service='inventory-api', version=os.getenv('APP_VERSION', 'dev'), status='running')

@app.get('/health')
def health():
    return jsonify(status='ok'), 200

@app.get('/api/items')
def items():
    return jsonify(items=ITEMS)
    # Lab dataset: in a real system this would be backed by a database.
    #return jsonify(items=[{'id': 1, 'name': 'router', 'stock': 8},
    #                     {'id': 2, 'name': 'switch', 'stock': 3}])

#Start of endpoint that can filter inventory items correctly
@app.get('/api/items/low-stock')
def low_stock():

    # Read threshold from URL
    threshold = request.args.get('threshold')

    # Check whether threshold was provided
    if threshold is None:
        return jsonify(error='threshold is required'), 400

    # Check whether threshold is an integer
    try:
        threshold = int(threshold)
    except ValueError:
        return jsonify(error='threshold must be an integer'), 400

    # Validate the allowed range
    if threshold < 0 or threshold > 100:
        return jsonify(error='threshold must be between 0 and 100'), 400

    # Find items whose stock is below the threshold
    low_stock_items = [
        item for item in ITEMS
        if item['stock'] < threshold
    ]

    # Return the results
    return jsonify(
        threshold=threshold,
        count=len(low_stock_items),
        items=low_stock_items
    ), 200
#End for endpoint can filter inventory items correctly
@app.get('/api/items/<int:item_id>')
def item_detail(item_id):
    item = next(
        (item for item in ITEMS if item['id'] == item_id),
        None
    )

    if item is None:
        return jsonify(error='item not found'), 404

    return jsonify(item), 200



#@app.get('/api/items/<int:item_id>')
#def item_detail(item_id):
#   data = {1: {'id': 1, 'name': 'router', 'stock': 8},
#           2: {'id': 2, 'name': 'switch', 'stock': 3}}
#   if item_id not in data:
#        return jsonify(error='item not found'), 404
#    return jsonify(data[item_id]), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
