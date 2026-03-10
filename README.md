# day_21_challenge
#folder structure
day21-challenge/
├── app/
│ ├── __init__.py
│ ├── models.py
│ ├── routes.py
│ └── database.py
├── tests/
│ ├── __init__.py
│ ├── test_unit.py
│ └── test_integration.py
├── requirements.txt
├── pytest.ini

Today's task: Writing Unit and Integration Tests!
- Created 3 unit tests for business logic
- Built 1 integration test with test database
- Used pytest and Flask for the implementation

   · Unit Test 1: User model creation
   · Unit Test 2: Product creation with valid price
   · Unit Test 3: Price validation (negative price raises error)
   · Integration Test: Signup endpoint with real database
