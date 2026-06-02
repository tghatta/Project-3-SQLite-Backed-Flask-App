from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProductInventory(db.Model):
    __tablename__ = 'product_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_cost = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "sku": self.sku,
            "name": self.name,
            "quantity": self.quantity,
            "unit_cost": self.unit_cost,
            "total_asset_value": round(self.quantity * self.unit_cost, 2)
        }
