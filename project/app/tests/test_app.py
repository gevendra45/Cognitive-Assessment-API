import json
import pytest
from app import create_app, db
from app.models.user import User
from app.models.journal import Journal

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def register_user(client, username='testuser', password='password'):
    return client.post('/users', json={'username': username, 'password': password})

def login_user(client, username='testuser', password='password'):
    return client.post('/login', json={'username': username, 'password': password})

def create_journal(client, token, text="I feel great and motivated"):
    return client.post(
        '/journals',
        json={'text': text},
        headers={'Authorization': f'Bearer {token}'}
    )

def test_register_user_success(client):
    response = register_user(client)
    assert response.status_code == 201
    assert b'User registered successfully' in response.data

def test_register_user_missing_fields(client):
    response = client.post('/users', json={'username': 'onlyuser'})
    assert response.status_code == 400
    assert b'Missing username or password' in response.data

def test_register_user_duplicate(client):
    register_user(client)
    response = register_user(client)
    assert response.status_code == 400
    assert b'Username already exists' in response.data

def test_login_user_success(client):
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data

def test_login_user_invalid(client):
    response = login_user(client)  # no registration
    assert response.status_code == 401
    assert b'Bad username or password' in response.data

def test_create_journal_success(client):
    register_user(client)
    login_resp = login_user(client)
    token = json.loads(login_resp.data)['access_token']

    response = create_journal(client, token)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'journal_id' in data
    assert 'score' in data

def test_create_journal_missing_text(client):
    register_user(client)
    login_resp = login_user(client)
    token = json.loads(login_resp.data)['access_token']

    response = client.post(
        '/journals',
        json={},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 400
    assert b'Journal text is required' in response.data

def test_get_journal_score_success(client):
    register_user(client)
    login_resp = login_user(client)
    token = json.loads(login_resp.data)['access_token']

    create_resp = create_journal(client, token)
    journal_id = json.loads(create_resp.data)['journal_id']

    response = client.get(
        f'/journals/{journal_id}/score',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'scores' in data

def test_get_journal_score_not_found(client):
    register_user(client)
    login_resp = login_user(client)
    token = json.loads(login_resp.data)['access_token']

    response = client.get(
        '/journals/9999/score',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 404
    assert b'Journal not found' in response.data
