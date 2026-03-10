from flask import request, jsonify
from .database import db
from .models import User, Product

def setup_routes(app):
    
    @app.route('/signup', methods=['POST'])
    def signup():
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'] # In real app, hash this!
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201
    
    @app.route('/products', methods=['POST'])
    def create_product():
        data = request.get_json()
        
        if not data or not data.get('name') or 'price' not in data:
            return jsonify({'error': 'Missing name or price'}), 400
        
        product = Product(name=data['name'], price=data['price'])
        
        try:
            product.validate_price()
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'message': 'Product created', 'product_id': product.id}), 201
    
    return app