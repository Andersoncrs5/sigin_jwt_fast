import pytest
from main import app
from fastapi.testclient import TestClient
from api.models.schemas.user_schema import CreateUserDTO, LoginDTO, UpdateUserDTO
import random

def test_get_user(client: TestClient):
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

    assert response_data['body']['token'] is not None

    token = response_data['body']['token']

    response_get_http = client.get(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response_get_http.status_code == 200
    response_get_body = response_get_http.json()

    assert response_get_body['code'] == 200
    assert response_get_body['message'] == 'User found with successfully'
    assert response_get_body['status'] == True
    assert response_get_body['body']['id'] is not None
    assert isinstance(response_get_body['body']['id'], int) == True
    assert response_get_body['body']['email'] == model['email']
    assert response_get_body['body']['name'] == model['name']
    
def test_delete_user(client: TestClient):
    num = random.randint(1,1000000)
 
    response = client.post(
        "/api/v1/auth/register",
        json=dict(CreateUserDTO(
            name = "user",
            email = f"user{num}@gmail.com",
            password = "12345678"
        ))
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data['body']['token'] is not None

    token = response_data['body']['token']

    response_get_http = client.delete(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response_get_http.status_code == 200
    response_get_body = response_get_http.json()

    assert response_get_body['code'] == 200
    assert response_get_body['message'] == 'Bye Bye'
    assert response_get_body['status'] == True
    assert response_get_body['body'] is None
    
def test_update_user(client: TestClient):
    num = random.randint(1,1000000)

    dto_create = dict(CreateUserDTO(
        name = "user",
        email = f"user{num}@gmail.com",
        password = "12345678"
    ))

    response = client.post(
        "/api/v1/auth/register",
        json=dto_create
    )

    assert response.status_code == 201
    response_data = response.json()

    assert response_data['body']['token'] is not None

    token = response_data['body']['token']

    dto = UpdateUserDTO(
        name = "user updated",
        password = None
    )

    response_update_http = client.put(
        "/api/v1/user",
        headers={"Authorization": f"Bearer {token}"},
        json=dict(dto)
    )
    
    assert response_update_http.status_code == 200
    response_get_body = response_update_http.json()

    assert response_get_body['code'] == 200
    assert response_get_body['message'] == "User updated with successfully"
    assert response_get_body['status'] == True
    assert response_get_body['body']['name'] == dto.name
    assert response_get_body['body']['email'] == dto_create['email']

    