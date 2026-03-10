import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_full_app
from app.database import db
from app.models import User, Product

@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_full_app()
    
    # Configure for testing - use in-memory SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Clean up
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

class TestIntegration:
    """Integration Test: Test real endpoints with test database"""
    
    def test_signup_endpoint(self, client):
        """Test user signup through real endpoint"""
        # Test data
        user_data = {
            'username': 'integrationuser',
            'email': 'integration@test.com',
            'password': 'testpass123'
        }
        
        # Make request to signup endpoint
        response = client.post('/signup', 
                              data=json.dumps(user_data),
                              content_type='application/json')
        
        # Check response
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'User created successfully'
        assert 'user_id' in data
        
        # Verify user was actually saved in database
        with client.application.app_context():
            user = User.query.filter_by(username='integrationuser').first()
            assert user is not None
            assert user.email == 'integration@test.com'
    
    def test_signup_duplicate_user(self, client):
        """Test signing up with existing username"""
        # First create a user
        user_data = {
            'username': 'duplicateuser',
            'email': 'first@test.com',
            'password': 'pass123'
        }
        client.post('/signup', 
                   data=json.dumps(user_data),
                   content_type='application/json')
        
        # Try to create same username with different email
        duplicate_data = {
            'username': 'duplicateuser',
            'email': 'different@test.com',
            'password': 'pass456'
        }
        response = client.post('/signup',
                              data=json.dumps(duplicate_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Username already exists'
    
    def test_create_product_endpoint(self, client):
        """Test product creation through endpoint"""
        product_data = {
            'name': 'Test Product',
            'price': 29.99
        }
        
        response = client.post('/products',
                              data=json.dumps(product_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Product created'
        
        # Verify in database
        with client.application.app_context():
            product = Product.query.filter_by(name='Test Product').first()
            assert product is not None
            assert product.price == 29.99
    
    def test_create_product_negative_price(self, client):
        """Test that endpoint rejects negative prices"""
        product_data = {
            'name': 'Invalid Product',
            'price': -10.00
        }
        
        response = client.post('/products',
                              data=json.dumps(product_data),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Price cannot be negative'