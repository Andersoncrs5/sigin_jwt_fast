import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from api.services.user_service import UserService
from api.models.entities.user_entity import UserEntity
from api.models.schemas.user_schema import UpdateUserDTO

mock_db_session = MagicMock(spec=Session)

@patch('api.services.user_service.UserRepository')
def test_get_by_id_with_valid_id(MockUserRepository, db_session: Session):

    mock_user = UserEntity(id=1, name="test user", email="test@gmail.com", password="hashed_password")

    MockUserRepository.return_value.get_by_id.return_value=mock_user

    user_service = UserService(db_session)

    user = user_service.get_by_id(1)

    assert user is not None
    assert user.id == 1
    assert user.name == mock_user.name
    assert user.email == mock_user.email

@patch('api.services.user_service.UserRepository')
def test_get_by_id_with_invalid_id(MockUserRepository, db_session: Session):
    
    user_service = UserService(db_session)

    user = user_service.get_by_id(0)

    assert user is None
    MockUserRepository.return_value.get_by_id.assert_not_called()

@patch('api.services.user_service.hash_password')
@patch('api.services.user_service.UserRepository')
def test_create_user(MockUserRepository, MockHashPassword, db_session: Session):
    
    MockHashPassword.return_value = "new_hashed_password"
    
    mock_user = UserEntity(id=1, name="New User", email="new@example.com", password="new_hashed_password")
    MockUserRepository.return_value.create.return_value = mock_user

    user_service = UserService(db_session)
    
    user_to_create = UserEntity(name="New User", email="new@example.com", password="password123")
    
    created_user = user_service.create(user_to_create)

    MockHashPassword.assert_called_once_with("password123")
    MockUserRepository.return_value.create.assert_called_once()

    assert user_to_create.password == "new_hashed_password"
    assert created_user.id == 1

@patch('api.services.user_service.UserRepository')
def test_delete_user(MockUserRepository, db_session: Session):
    user_service = UserService(db_session)
    mock_user = UserEntity(id=1, name="User to Delete")

    user_service.delete(mock_user)

    MockUserRepository.return_value.delete.assert_called_once_with(mock_user)

@patch('api.services.user_service.hash_password')
@patch('api.services.user_service.UserRepository')
def test_update_user(MockUserRepository, MockHashPassword, db_session: Session):
    MockHashPassword.return_value = "new_hashed_password"
    
    mock_user = UserEntity(id=1, name="Old Name", email="user@example.com", password="old_hashed_password")
    
    dto = UpdateUserDTO(name="New Name", password="new_password")
    
    updated_mock_user = UserEntity(id=1, name="New Name", email="user@example.com", password="new_hashed_password")
    MockUserRepository.return_value.update.return_value = updated_mock_user
    
    user_service = UserService(db_session)
    
    updated_user = user_service.update(mock_user, dto)

    MockHashPassword.assert_called_once_with("new_password")

    assert mock_user.password == "new_hashed_password"
    assert mock_user.name == "New Name"

    MockUserRepository.return_value.update.assert_called_once()

    assert updated_user.name == "New Name"
    assert updated_user.password == "new_hashed_password"