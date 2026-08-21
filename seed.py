import json
import os
from app import app
from models import db, User, Product, ProductSpecification

def seed_database():
    """
    Reads existing JSON files and populates relational database tables
    while preserving existing relationships and data integrity.
    """
    with app.app_context():
        # 1. Migrate Users
        users_file = 'users.json'
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                imported_users_count = 0
                for item in users_data:
                    existing_user = User.query.filter_by(email=item['email']).first()
                    if not existing_user:
                        user = User(
                            username=item['username'],
                            email=item['email'],
                            password_hash=item['password'],
                            role=item.get('role', 'user').lower()
                        )
                        db.session.add(user)
                        imported_users_count += 1
                
                db.session.commit()
                print(f"[+] Successfully migrated {imported_users_count} users.")
        else:
            print(f"[-] '{users_file}' not found. Skipping user migration.")

        # 2. Migrate Products and Specifications
        products_file = 'file.json'
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                products_data = json.load(f)
                imported_products_count = 0
                for item in products_data:
                    existing_product = Product.query.get(item['id'])
                    if not existing_product:
                        product = Product(
                            id=item['id'],
                            name=item['name'],
                            image_url=item['image_url'],
                            description=item['description'],
                            price_usd=item['price_usd'],
                            condition=item.get('condition', 'New')
                        )

                        # Extract flattened specifications dynamically into normalized records
                        for i in range(1, 5):
                            title_key = f'spec_title_{i}'
                            spec_key = f'specification_{i}'
                            if title_key in item and spec_key in item:
                                spec = ProductSpecification(
                                    spec_title=item[title_key],
                                    specification=item[spec_key]
                                )
                                product.specifications.append(spec)

                        db.session.add(product)
                        imported_products_count += 1

                db.session.commit()
                print(f"[+] Successfully migrated {imported_products_count} products with specifications.")
        else:
            print(f"[-] '{products_file}' not found. Skipping product migration.")

if __name__ == '__main__':
    seed_database()
