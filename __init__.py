from flask import Flask, request, jsonify
from models import db, ProductInventory

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/api/inventory', methods=['GET'])
    def get_inventory():
        items = ProductInventory.query.all()
        return jsonify([item.to_dict() for item in items]), 200

    @app.route('/api/inventory', methods=['POST'])
    def add_inventory_item():
        data = request.get_json() or {}
        required = ['sku', 'name', 'unit_cost']
        if not all(k in data for k in required):
            return jsonify({"error": "Missing required fields (sku, name, unit_cost)"}), 400
            
        if ProductInventory.query.filter_by(sku=data['sku']).first():
            return jsonify({"error": "SKU already exists"}), 400

        item = ProductInventory(
            sku=data['sku'],
            name=data['name'],
            quantity=data.get('quantity', 0),
            unit_cost=data['unit_cost']
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201

    return app
