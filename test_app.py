import pytest
import json
from app import app, db, Task

@pytest.fixture
def client():
    """Setup test client with a fresh database for each test."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_tasks.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest 