from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_usd = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), default='New', nullable=False)
    stock = db.Column(db.Integer, default=1, nullable=False)  # المخزون / الكمية المتاحة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    specifications = db.relationship(
        'ProductSpecification',
        backref='product',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __repr__(self):
        return f'<Product {self.name}>'


class ProductSpecification(db.Model):
    __tablename__ = 'product_specifications'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    spec_title = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Spec {self.spec_title}: {self.specification}>'