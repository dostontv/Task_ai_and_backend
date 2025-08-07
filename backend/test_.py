import os

import pytest
import requests
from dotenv import load_dotenv
from starlette import status


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


def test_tests():
    api_key = os.getenv('API_KEY')
    data = requests.get(f'http://localhost:8000/tests?api_key={api_key}')
    assert data.status_code == status.HTTP_200_OK
    assert isinstance(data.json(), list)


def test_results():
    api_key = os.getenv('API_KEY')
    data = {
        'test_id': 2,
        'user_id': 2,
        'score': 2.3
    }
    response = requests.post(f'http://localhost:8000/results?api_key={api_key}', json=data)
    print(response.json())

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert isinstance(response, dict)
    assert len(response) == 3
