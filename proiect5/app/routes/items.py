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
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'review' not in data:
        return jsonify({'eroare': 'Date invalide'}), 400

    # Validare pentru review (permițând valori decimale)
    try:
        review = float(data['review'])
        if not (1.0 <= review <= 5.0):
            return jsonify({'eroare': 'Review-ul trebuie să fie între 1.0 și 5.0'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Review-ul trebuie să fie un număr'}), 400

    items = load_data()
    new_id = max([i['id'] for i in items], default=0) + 1
    data['id'] = new_id
    items.append(data)
    save_data(items)
    return jsonify(data), 201


@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data or 'review' not in data:
        return jsonify({'eroare': 'Date invalide'}), 400

    # Validare pentru review (permițând valori decimale)
    try:
        review = float(data['review'])
        if not (1.0 <= review <= 5.0):
            return jsonify({'eroare': 'Review-ul trebuie să fie între 1.0 și 5.0'}), 400
    except (ValueError, TypeError):
        return jsonify({'eroare': 'Review-ul trebuie să fie un număr'}), 400

    items = load_data()
    for i in items:
        if i['id'] == item_id:
            i.update(data)
            save_data(items)
            return jsonify(i), 200
    return jsonify({'eroare': 'Articolul nu a fost găsit'}), 404


@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()
    items_new = [i for i in items if i['id'] != item_id]
    if len(items_new) == len(items):
        return jsonify({'eroare': 'Articolul nu a fost găsit'}), 404
    save_data(items_new)
    return jsonify({'mesaj': 'Articolul a fost șters'}), 200

