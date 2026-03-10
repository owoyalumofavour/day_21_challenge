import pytest
from app.models import User, Product
from app.database import db
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestUserModel:
    """Unit Test 1: Test User Model Logic"""
    
    def test_user_creation(self):
        """Test that a user object can be created with correct attributes"""
        user = User(
            username="testuser",
            email="test@example.com",
            password="securepass123"
        )
        
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "securepass123"
        assert user.id is None # ID is None until saved to database

class TestProductModel:
    """Unit Test 2 & 3: Test Product Model Logic"""
    
    def test_product_creation_with_valid_price(self):
        """Test product creation with valid positive price"""
        product = Product(name="Laptop", price=999.99)
        assert product.name == "Laptop"
        assert product.price == 999.99
    
    def test_product_price_cannot_be_negative(self):
        """Test that validation raises error for negative price"""
        product = Product(name="Invalid Product", price=-50.00)
        
        with pytest.raises(ValueError, match="Price cannot be negative"):
            product.validate_price()
    
    def test_product_with_zero_price(self):
        """Test edge case: zero price (should be valid)"""
        product = Product(name="Free Item", price=0.00)
        assert product.validate_price() is True # Should pass

class TestUtilityFunctions:
    """Additional unit tests for any utility functions"""
    
    def test_price_formatting(self):
        """Test a utility function (if you had one)"""
        # This is just a demonstration - you could add more complex logic
        def format_price(price):
            return f"${price:.2f}"
        
        assert format_price(10.5) == "$10.50"
        assert format_price(0) == "$0.00"
        assert format_price(99.99) == "$99.99"