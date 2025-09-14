import pytest
from main import app
from fastapi.testclient import TestClient
from api.models.schemas.user_schema import CreateUserDTO, LoginDTO
import random

def test_throw_status_conflict_auth(client: TestClient):
    num = random.randint(1,1000000)

    model = dict(CreateUserDTO(
        name = "user",
        email = f"user{num}@gmail.com",
        password = "12345678"
    ))

    response = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response.status_code == 201

    response_conflict = client.post(
        "/api/v1/auth/register",
        json=model
    )
    
    assert response_conflict.status_code == 409

    response_body = response_conflict.json()

    assert response_body['code'] == 409
    assert response_body['message'] == "Email already in use"
    assert response_body['status'] == False
    assert response_body['body'] is None

def test_create_auth(client: TestClient):
    num = random.randint(1,1000000)

    model = dict(CreateUserDTO(
        name = "user",
        email = f"user{num}@gmail.com",
        password = "12345678"
    ))

    response = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data['code'] == 201
    assert response_data['message'] == "Welcome"
    assert response_data['status'] == True
    assert response_data['body']['token'] is not None
    assert response_data['body']['refresh_token'] is not None
    
def test_login_auth(client: TestClient):
    num = random.randint(1,1000000)

    model = dict(CreateUserDTO(
        name = "user",
        email = f"user{num}@gmail.com",
        password = "12345678"
    ))

    client.post(
        "/api/v1/auth/register",
        json=model
    )

    model_login = dict(LoginDTO(
        email = model["email"],
        password = model["password"],
    ))

    response = client.post(
        "/api/v1/auth/login",
        json=model_login
    )

    assert response.status_code == 200
    response_data = response.json()

    assert response_data['message'] == 'Welcome again'
    assert response_data['code'] == 200
    assert response_data['status'] == True
    assert response_data['body']['token'] is not None
    assert response_data['body']['refresh_token'] is not None

def test_revoke_auth(client: TestClient):
    num = random.randint(1,1000000)

    model = dict(CreateUserDTO(
        name = "user",
        email = f"user{num}@gmail.com",
        password = "12345678"
    ))

    response = client.post(
        "/api/v1/auth/register",
        json=model
    )

    assert response.status_code == 201
    respnse_json_create = response.json()
    assert respnse_json_create['body']['token'] is not None
    token = str(respnse_json_create['body']['token'])

    response = client.get(
        "/api/v1/auth/revoke",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    response_body = response.json()

    assert response_body['message'] == 'Bye Bye'
    assert response_body['code'] == 200
    assert response_body['status'] == True
    assert response_body['body'] is None

def test_refresh_token_auth(client: TestClient):
    num = random.randint(1,1000000)

    response = client.post(
        "/api/v1/auth/register",
        json=dict(CreateUserDTO(
            name = "user",
            email = f"user{num}@gmail.com",
            password = "12345678"
        )
    ))

    assert response.status_code == 201
    respnse_json_create = response.json()
    assert respnse_json_create['body']['token'] is not None
    token = str(respnse_json_create['body']['token'])
    refresh_token = str(respnse_json_create['body']['refresh_token'])

    response_http = client.get(
        f"/api/v1/auth/{refresh_token}",
    )

    response_body = response_http.json()

    assert response_http.status_code == 200
    assert response_body['message'] == "New Tokens sended"
    assert response_body['code'] == 200
    assert response_body['status'] == True
    assert response_body['body']['token'] is not None
    assert response_body['body']['refresh_token'] is not None
