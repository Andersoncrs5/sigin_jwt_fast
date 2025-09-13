from pydantic import BaseModel

class CreateUserDTO(BaseModel):
    name: str
    email: str
    password: str

class UpdateUserDTO(BaseModel):
    name: str | None
    password: str | None
