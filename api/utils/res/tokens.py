from pydantic import BaseModel

class Tokens(BaseModel):
    token: str
    refresh_token: str