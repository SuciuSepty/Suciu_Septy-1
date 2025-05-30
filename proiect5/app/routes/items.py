import json
import os
from flask import Blueprint, jsonify, request, render_template

items_bp = Blueprint('items', __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/items.json')


def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def reindex_and_save_data(items_list):
    for index, item in enumerate(items_list):
        item['id'] = index + 1
    save_data(items_list)
    return items_list


@items_bp.route('/')
def index():
    return render_template('index.html')


@items_bp.route('/items', methods=['GET'])
def get_items():
    return jsonify(load_data()), 200


@items_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = load_data()
    item = next((i for i in items if i['id'] == item_id), None)
    if item:
        return jsonify(item), 200
    return jsonify({'eroare': 'Articolul nu a fost găsit'}), 404


@items_bp.route('/items', methods=['POST'])
def create_item():
    request_data = request.get_json()
    if not request_data or 'name' not in request_data or 'price' not in request_data or 'review' not in request_data:
        return jsonify({'eroare': 'Date invalide'}), 400

    try:
        review = float(request_data['review'])
        if not (1.0 <= review <= 5.0):
            return jsonify({'eroare': 'Review-ul trebuie să fie între 1.0 și 5.0'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Review-ul trebuie să fie un număr'}), 400
    
    try:
        price = float(request_data['price'])
        if price < 0:
            return jsonify({'eroare': 'Prețul nu poate fi negativ'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Prețul trebuie să fie un număr'}), 400

    items = load_data()
    
    new_item = {
        'name': request_data['name'],
        'price': price,
        'review': review
        # ID will be assigned by reindex_and_save_data
    }
    items.append(new_item)
    
    reindex_and_save_data(items) # This re-indexes and saves, new_item gets its ID here
    
    # new_item reference now points to the item in the list with its assigned ID
    return jsonify(new_item), 201


@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    request_data = request.get_json()
    if not request_data or 'name' not in request_data or 'price' not in request_data or 'review' not in request_data:
        return jsonify({'eroare': 'Date invalide'}), 400

    try:
        review = float(request_data['review'])
        if not (1.0 <= review <= 5.0):
            return jsonify({'eroare': 'Review-ul trebuie să fie între 1.0 și 5.0'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Review-ul trebuie să fie un număr'}), 400

    try:
        price = float(request_data['price'])
        if price < 0:
            return jsonify({'eroare': 'Prețul nu poate fi negativ'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Prețul trebuie să fie un număr'}), 400

    items = load_data()
    item_to_update = None
    for i in items:
        if i['id'] == item_id:
            i['name'] = request_data['name']
            i['price'] = price
            i['review'] = review
            item_to_update = i # Keep reference to the item
            break
    
    if item_to_update:
        reindex_and_save_data(items) # Re-index and save
        # item_to_update will have its potentially new ID
        return jsonify(item_to_update), 200
    
    return jsonify({'eroare': 'Articolul nu a fost găsit'}), 404


@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()
    original_length = len(items)
    items_after_deletion = [i for i in items if i['id'] != item_id]
    
    if len(items_after_deletion) == original_length:
        return jsonify({'eroare': 'Articolul nu a fost găsit'}), 404
        
    reindex_and_save_data(items_after_deletion)
    return jsonify({'mesaj': 'Articolul a fost șters'}), 200

