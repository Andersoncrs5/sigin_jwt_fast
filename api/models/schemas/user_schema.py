from pydantic import BaseModel, Field, EmailStr
from api.models.entities.user_entity import UserEntity

class CreateUserDTO(BaseModel):
    name: str = Field(..., min_length=4, max_length=50, description="The name field should be between 4 and 50")
    email: EmailStr = Field(..., min_length=8, max_length=150, description="The email field should be between 8 and 150")
    password: str = Field(..., min_length=6, max_length=50, description="The password field should be between 6 and 50")

    def to_user_entity(self) -> UserEntity:
        return UserEntity(
            name= self.name,
            email= self.email,
            password= self.password,
        )
    
class UpdateUserDTO(BaseModel):
    name: str | None = Field(None, max_length=50, description="The name field should have size max of 50")
    password: str | None = Field(None, max_length=50, description="The password field should have size max of 50")

class LoginDTO(BaseModel):
    email: EmailStr = Field(..., min_length=8, max_length=150, description="The email field should be between 8 and 150")
    password: str = Field(..., min_length=6, max_length=50, description="The password field should be between 6 and 50")

class UserOUT(BaseModel):
    id: int
    name: str
    email: str