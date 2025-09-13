from pydantic import BaseModel
from api.models.entities.user_entity import UserEntity

class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str

    def to_user_entity(self) -> UserEntity:
        return UserEntity(
            name= self.name,
            email= self.email,
            password= self.password,
        )
    

class UpdateUserDTO(BaseModel):
    name: str | None
    password: str | None

class LoginDTO(BaseModel):
    email: str
    password: str