from api.models.entities.user_entity import UserEntity
from sqlalchemy.orm import Session
from api.models.schemas.user_schema import UpdateUserDTO
from api.services.crypto_service import hash_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> (UserEntity | None) :
        if user_id <= 0 :
            return None
        
        return self.db.query(UserEntity).filter(UserEntity.id == user_id).first()

    def exists_by_email(self, email: str) -> bool:
        if email == "" :
            return False

        return self.db.query(UserEntity).filter(UserEntity.email == email).count() > 0

    def get_by_email(self, email: str) -> (UserEntity | None) :
        if email == "" :
            return None

        return self.db.query(UserEntity).filter(UserEntity.email == email).first()

    def create(self, user: UserEntity) -> UserEntity:
        user.password = hash_password(user.password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user

    def delete(self, user: UserEntity):
        self.db.delete(user)
        self.db.commit()

    def refresh_token(self, refresh_token: str, user: UserEntity)  -> (UserEntity):
        if refresh_token == "":
            return user

        user.refresh_token = refresh_token

        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: UserEntity, dto: UpdateUserDTO) -> UserEntity:
        if dto.name != None :
            user.name = dto.name

        if dto.password != None :
            user.password = hash_password(dto.password)

        self.db.commit()
        self.db.refresh(user)
        return user