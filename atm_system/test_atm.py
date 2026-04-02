import pytest
from app import app, db, User, Transaction

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

def test_index_redirects(client):
    rv = client.get('/')
    assert rv.status_code == 302

def test_register_and_login(client):
    rv = client.post('/login', data={'action': 'register', 'username': 'testuser', 'pin': '1234'})
    assert b'Account created' in rv.data or rv.status_code == 302

    rv = client.post('/login', data={'action': 'login', 'username': 'testuser', 'pin': '1234'}, follow_redirects=True)
    assert b'Current Balance' in rv.data

def test_deposit_and_withdraw(client):
    client.post('/login', data={'action': 'register', 'username': 'user1', 'pin': '123'})
    client.post('/login', data={'action': 'login', 'username': 'user1', 'pin': '123'})

    rv = client.post('/dashboard', data={'action': 'deposit', 'amount': '100'}, follow_redirects=True)
    assert b'100.00' in rv.data

    rv = client.post('/dashboard', data={'action': 'withdraw', 'amount': '40'}, follow_redirects=True)
    assert b'60.00' in rv.data
