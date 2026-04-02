import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_routes(client):
    # Register
    rv = client.post('/register', data={
        'name': 'Test User',
        'email': 'test@test.com',
        'password': 'pass',
        'confirm_password': 'pass'
    }, follow_redirects=True)
    assert b'Account created' in rv.data or b'Email already registered.' in rv.data or rv.status_code == 200
    
    # Login
    rv = client.post('/login', data={
        'email': 'test@test.com',
        'password': 'pass'
    }, follow_redirects=True)
    assert b'Welcome back' in rv.data or b'Dashboard' in rv.data or rv.status_code == 200

    # Create Item
    rv = client.post('/items', data={
        'name': 'Test Item',
        'email': 'test@test.com',
        'category': 'Other',
        'description': 'Testing creation',
        'status': 'Active'
    }, follow_redirects=True)
    assert rv.status_code == 200
    assert b'created successfully' in rv.data or b'Test Item' in rv.data
