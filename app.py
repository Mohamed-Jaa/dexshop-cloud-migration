from functools import wraps
from flask import Flask, render_template, url_for, request, redirect, session, flash , jsonify
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config
from models import db, User, Product, ProductSpecification

from utils.storage import upload_file_to_storage

from ai_helper import generate_product_metadata

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and migration engine
db.init_app(app)
migrate = Migrate(app, db)


def admin_required(f):
    """
    Decorator to enforce role-based access control for administrative endpoints.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or session['user'].get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def main():
    featured_products = Product.query.order_by(Product.id.asc()).limit(4).all()
    return render_template('main.html', featured_products=featured_products)


@app.route('/index')
@app.route('/products/<int:page>')
def index(page=1):
    per_page = app.config.get('ITEMS_PER_PAGE', 12)
    pagination = Product.query.order_by(Product.id.asc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template(
        'index.html',
        products=pagination.items,
        total_pages=pagination.pages,
        current_page=page
    )


@app.route('/product/<int:product_id>')
def product(product_id):
    product_data = db.session.get(Product, product_id)
    if not product_data:
        flash('Product not found.', 'error')
        return redirect(url_for('index'))

    related_products = Product.query.filter(Product.id != product_id).limit(4).all()
    return render_template(
        'product.html',
        product=product_data,
        related_products=related_products
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        submitted_email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Database-level unique check
        if User.query.filter_by(email=submitted_email).first():
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html', form_data=request.form)

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=submitted_email,
            password_hash=hashed_password,
            role='user'
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        submitted_email = request.form.get('email', '').strip()
        submitted_password = request.form.get('password', '')

        user = User.query.filter_by(email=submitted_email).first()

        if user and check_password_hash(user.password_hash, submitted_password):
            session['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
            flash('Login successful!', 'success')
            if user.role == 'admin':
                return redirect(url_for('dashboard'))
            return redirect(url_for('index'))

        flash('Invalid email or password. Please try again.', 'error')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('main'))


# -------------------------------------------------------------
# Admin Dashboard & Management Routes
# -------------------------------------------------------------

@app.route('/dashboard', methods=['GET', 'POST'])
@admin_required
def dashboard():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        price_usd = request.form.get('price_usd', '').strip()
        condition = request.form.get('condition', 'New')
        stock = request.form.get('stock', '1').strip()
        description = request.form.get('description', '').strip()
        image_file = request.files.get('image')

        if not name or not price_usd or not description or not image_file:
            flash('All product fields and an image are required.', 'error')
            return redirect(url_for('dashboard'))

        try:
            stock_val = max(0, int(stock))
            uploaded_image_url = upload_file_to_storage(image_file)
            if not uploaded_image_url:
                flash('Invalid image file.', 'error')
                return redirect(url_for('dashboard'))

            new_product = Product(
                name=name,
                image_url=uploaded_image_url,
                description=description,
                price_usd=price_usd,
                condition=condition,
                stock=stock_val
            )

            for i in range(1, 5):
                spec_title = request.form.get(f'spec_title_{i}', '').strip()
                spec_desc = request.form.get(f'spec_desc_{i}', '').strip()
                if spec_title and spec_desc:
                    spec = ProductSpecification(
                        spec_title=spec_title,
                        specification=spec_desc
                    )
                    new_product.specifications.append(spec)

            db.session.add(new_product)
            db.session.commit()

            flash('Product added successfully to inventory!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error adding product: {str(e)}', 'error')
            return redirect(url_for('dashboard'))

    # Fetch stats and listing
    products = Product.query.order_by(Product.id.desc()).all()
    users = User.query.order_by(User.id.asc()).all()
    total_stock = sum(p.stock for p in products)

    return render_template(
        'dashboard.html',
        products=products,
        users=users,
        total_products=len(products),
        total_users=len(users),
        total_stock=total_stock
    )


@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name', product.name).strip()
        product.price_usd = request.form.get('price_usd', product.price_usd).strip()
        product.condition = request.form.get('condition', product.condition)
        product.description = request.form.get('description', product.description).strip()
        product.stock = max(0, int(request.form.get('stock', product.stock)))

        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            new_url = upload_file_to_storage(image_file)
            if new_url:
                product.image_url = new_url

        # Update or recreate specs
        ProductSpecification.query.filter_by(product_id=product.id).delete()
        for i in range(1, 5):
            spec_title = request.form.get(f'spec_title_{i}', '').strip()
            spec_desc = request.form.get(f'spec_desc_{i}', '').strip()
            if spec_title and spec_desc:
                db.session.add(ProductSpecification(
                    product_id=product.id,
                    spec_title=spec_title,
                    specification=spec_desc
                ))

        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_product.html', product=product)


@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{product.name}" deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/user/toggle-role/<int:user_id>', methods=['POST'])
@admin_required
def toggle_user_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session.get('user_id'):
        flash('You cannot change your own role.', 'error')
        return redirect(url_for('dashboard'))

    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    flash(f'Updated role for {user.username} to {user.role}.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == session.get('user_id'):
        flash('You cannot delete your own admin account.', 'error')
        return redirect(url_for('dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user.username}" deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash("Thank you! Your message has been sent successfully. We will reply shortly.", 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')

from werkzeug.security import generate_password_hash

@app.route('/admin/user/create', methods=['POST'])
@admin_required
def create_user():
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()
    role = request.form.get('role', 'user')

    if not username or not email or not password:
        flash('Username, email, and password are required.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/api/ai-autofill', methods=['POST'])
def ai_autofill():
    product_name = request.form.get('name', '').strip()
    image_file = request.files.get('image')

    if not product_name and not image_file:
        return jsonify({'error': 'Please provide at least a product name or image'}), 400

    image_bytes = None
    mime_type = "image/jpeg"

    if image_file and image_file.filename != '':
        image_bytes = image_file.read()
        mime_type = image_file.mimetype or "image/jpeg"

    ai_data = generate_product_metadata(product_name, image_bytes, mime_type)

    if not ai_data:
        return jsonify({'error': 'AI failed to generate details'}), 500

    return jsonify(ai_data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000) # nosec B104
