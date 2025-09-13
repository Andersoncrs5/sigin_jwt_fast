from sqlalchemy.orm import Session
from api.models.entities.user_entity import UserEntity
from api.repositories.user_repository import UserRepository 
from api.models.schemas.user_schema import UpdateUserDTO
from api.services.crypto_service import hash_password

class UserService():
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: int) -> (UserEntity | None):
        if user_id <= 0:
            return None

        return self.repository.get_by_id(user_id)

    def delete(self, user: UserEntity):
        self.repository.delete(user)
        
    def get_by_email(self, email: str) -> (UserEntity | None):
        if email == "":
            return None

        return self.repository.get_by_email(email)
    
    def exists_by_email(self, email: str) -> bool:
        if email == "":
            return False

        return self.repository.exists_by_email(email)

    def create(self, user: UserEntity) -> UserEntity:
        user.password = hash_password(user.password)

        return self.repository.create(user)
    
    def set_refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        return self.repository.refresh_token(refresh_token, user)

    def update(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        if dto.name != None :
            user.name = dto.name

        if dto.password != None :
            user.password = hash_password(dto.password)

        return self.repository.update(user)