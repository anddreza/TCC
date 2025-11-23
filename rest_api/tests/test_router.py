from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import pytest
from main import app
import json
import pytest
import os

@pytest.fixture(autouse=True)
def set_test_env():
    """Set environment variables for testing"""
    os.environ['ALLOW_ORIGIN'] = 'http://localhost:3000'
    os.environ['MONGO_URI'] = 'mongodb://localhost:27017'
    os.environ['GOOGLE_API_KEY'] = 'fake-api-key'

@pytest.fixture
def client():
    with patch('routers.properties.get_properties_collection') as mock_get_collection:
        mock_col = Mock()
        mock_get_collection.return_value = mock_col
        yield TestClient(app)

@pytest.fixture
def fake_property():
    with open('tests/fake.json', 'r') as f:
        return json.load(f)

@pytest.fixture
def mock_collection():
    with patch('routers.properties.get_properties_collection') as mock_get_collection:
        mock_col = Mock()
        mock_get_collection.return_value = mock_col
        yield mock_col

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"example_result": True}

def test_properties(client, fake_property, mock_collection):
    mock_collection.find_one.return_value = fake_property
    response = client.get(f"/properties/{fake_property['_id']}")
    assert response.status_code == 200
    assert response.json() == fake_property    