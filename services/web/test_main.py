from fastapi.testclient import testclient
from .main import app

def test_read_main():
    response = client.post(
        "/token", 
        json={
            "username":"maxence",
            "password":"maxence"
        })
    assert response.status_code == 200
